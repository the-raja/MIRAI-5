import React from 'react';

interface HealthBarProps {
  currentHp: number;
  maxHp?: number;
  label: string;
  variant?: 'boss' | 'player';
}

export const HealthBar: React.FC<HealthBarProps> = ({
  currentHp,
  maxHp = 100,
  label,
  variant = 'player',
}) => {
  const pct = Math.max(0, Math.min(100, (currentHp / maxHp) * 100));
  const fillStyle =
    variant === 'boss'
      ? 'bg-gradient-to-r from-red-600 to-amber-500'
      : 'bg-gradient-to-r from-blue-600 to-emerald-500';

  return (
    <div className="flex flex-col gap-1.5 w-full font-mono text-xs">
      <div className="flex justify-between items-center font-semibold">
        <span className="text-slate-300">{label}</span>
        <span className={variant === 'boss' ? 'text-red-400' : 'text-blue-400'}>
          {currentHp} / {maxHp}
        </span>
      </div>
      <div className="w-full bg-slate-950 h-3.5 rounded-full overflow-hidden border border-slate-800 p-0.5">
        <div
          className={`h-full rounded-full transition-all duration-300 ${fillStyle}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
};
