"""DatasetManager module for ML Infrastructure.

Centralized single source of truth for ML datasets:
- Dataset versioning
- Train / Validation / Test data splitting
- Dataset Metadata schema
- Feature & Label names management
- Normalization hooks for numerical ML features
"""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field
import time
import random
import os
import csv


class DatasetMetadata(BaseModel):
    dataset_id: str
    version: str = "v1.0.0"
    timestamp: float = Field(default_factory=time.time)
    num_samples: int = 0
    feature_names: List[str] = Field(default_factory=list)
    label_names: List[str] = Field(default_factory=list)
    split_ratios: Dict[str, float] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DatasetSplit(BaseModel):
    train_data: List[Dict[str, Any]] = Field(default_factory=list)
    val_data: List[Dict[str, Any]] = Field(default_factory=list)
    test_data: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: DatasetMetadata


class DatasetManager:
    def __init__(self, dataset_dir: str = r"backend/data/datasets") -> None:
        self.dataset_dir = dataset_dir
        os.makedirs(self.dataset_dir, exist_ok=True)
        self.metadata_store: Dict[str, DatasetMetadata] = {}

    def create_split(
        self,
        rows: List[Dict[str, Any]],
        dataset_id: str = "ds_intent_01",
        version: str = "v1.0.0",
        train_ratio: float = 0.8,
        val_ratio: float = 0.1,
        test_ratio: float = 0.1,
        shuffle: bool = True
    ) -> DatasetSplit:
        """Splits raw dataset rows into Train, Validation, and Test subsets."""
        if not rows:
            meta = DatasetMetadata(dataset_id=dataset_id, version=version, num_samples=0)
            return DatasetSplit(metadata=meta)

        data = list(rows)
        if shuffle:
            random.seed(42)
            random.shuffle(data)

        total = len(data)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)

        train_data = data[:train_end]
        val_data = data[train_end:val_end]
        test_data = data[val_end:]

        sample_row = rows[0]
        feature_names = [k for k in sample_row.keys() if k != "target_next_action"]
        label_names = ["target_next_action"]

        meta = DatasetMetadata(
            dataset_id=dataset_id,
            version=version,
            num_samples=total,
            feature_names=feature_names,
            label_names=label_names,
            split_ratios={"train": train_ratio, "val": val_ratio, "test": test_ratio}
        )
        self.metadata_store[dataset_id] = meta

        return DatasetSplit(
            train_data=train_data,
            val_data=val_data,
            test_data=test_data,
            metadata=meta
        )

    def apply_normalization_hooks(
        self,
        rows: List[Dict[str, Any]],
        feature_keys: List[str]
    ) -> List[Dict[str, Any]]:
        """Applies Min-Max normalization hooks to specified numerical feature columns."""
        if not rows or not feature_keys:
            return rows

        normalized_rows: List[Dict[str, Any]] = []
        ranges: Dict[str, Tuple[float, float]] = {}

        for key in feature_keys:
            vals = [float(r[key]) for r in rows if key in r and isinstance(r[key], (int, float))]
            if vals:
                min_v, max_v = min(vals), max(vals)
                ranges[key] = (min_v, max_v if max_v > min_v else min_v + 1.0)

        for r in rows:
            new_r = dict(r)
            for key, (min_v, max_v) in ranges.items():
                if key in new_r and isinstance(new_r[key], (int, float)):
                    new_r[f"{key}_normalized"] = round((float(new_r[key]) - min_v) / (max_v - min_v), 4)
            normalized_rows.append(new_r)

        return normalized_rows
