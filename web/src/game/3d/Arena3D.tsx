'use client';

import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';

function Ground() {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
      <planeGeometry args={[30, 20]} />
      <meshStandardMaterial color="#0f172a" roughness={0.8} metalness={0.2} />
    </mesh>
  );
}

function Pillar() {
  return (
    <mesh position={[0, 1.5, 0]} castShadow receiveShadow>
      <boxGeometry args={[1.5, 3, 1.5]} />
      <meshStandardMaterial color="#475569" roughness={0.4} />
    </mesh>
  );
}

function PlayerMesh() {
  const meshRef = useRef<THREE.Mesh>(null);

  return (
    <mesh ref={meshRef} position={[-5, 1, 0]} castShadow>
      <sphereGeometry args={[0.8, 32, 32]} />
      <meshStandardMaterial color="#3b82f6" emissive="#1e40af" emissiveIntensity={0.3} />
    </mesh>
  );
}

function BossMesh() {
  const meshRef = useRef<THREE.Mesh>(null);

  return (
    <mesh ref={meshRef} position={[5, 1, 0]} castShadow>
      <sphereGeometry args={[1.1, 32, 32]} />
      <meshStandardMaterial color="#ef4444" emissive="#991b1b" emissiveIntensity={0.3} />
    </mesh>
  );
}

export default function Arena3D() {
  return (
    <div className="w-full h-80 bg-slate-950 rounded-xl overflow-hidden border border-slate-800 relative">
      <Canvas shadows>
        <PerspectiveCamera makeDefault position={[0, 12, 16]} fov={50} />
        <OrbitControls enableZoom={false} maxPolarAngle={Math.PI / 2.2} />

        <ambientLight intensity={0.4} />
        <directionalLight
          position={[10, 20, 15]}
          intensity={1.2}
          castShadow
          shadow-mapSize-width={1024}
          shadow-mapSize-height={1024}
        />
        <pointLight position={[0, 5, 0]} color="#3b82f6" intensity={2} distance={10} />

        <Ground />
        <Pillar />
        <PlayerMesh />
        <BossMesh />
      </Canvas>
    </div>
  );
}
