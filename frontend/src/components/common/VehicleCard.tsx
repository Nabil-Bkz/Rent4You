'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Vehicle } from '@/lib/api/vehicles';

interface VehicleCardProps {
  vehicle: Vehicle;
}

export default function VehicleCard({ vehicle }: VehicleCardProps) {
  return (
    <div className="card" style={{
      textAlign: 'center',
      padding: '3rem 2rem',
      borderRadius: '0.5rem',
      outline: 'var(--outline)',
      outlineOffset: '-1rem',
      boxShadow: 'var(--box-shadow)',
      transition: '0.2s linear',
      cursor: 'pointer',
    }}>
      {vehicle.image_url && (
        <div style={{ height: '20rem', marginBottom: '1rem', position: 'relative' }}>
          <img
            src={vehicle.image_url}
            alt={`${vehicle.marque} ${vehicle.model}`}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              borderRadius: '0.5rem',
            }}
          />
        </div>
      )}
      
      <h3 style={{ fontSize: '2.5rem', color: 'var(--black)', marginBottom: '1rem' }}>
        {vehicle.marque} {vehicle.model}
      </h3>
      
      <p style={{ fontSize: '1.5rem', color: 'var(--light-color)', marginBottom: '1rem' }}>
        {vehicle.description.substring(0, 100)}...
      </p>
      
      <div style={{ fontSize: '2rem', color: 'var(--light-color)', marginBottom: '1rem' }}>
        {vehicle.prix_jour}€/jour
      </div>
      
      <div style={{ marginBottom: '1rem' }}>
        <span style={{ fontSize: '1.7rem', color: 'var(--orange)' }}>★★★★★</span>
      </div>
      
      <Link href={`/vehicles/${vehicle.id}`} className="btn">
        Voir détails
      </Link>
    </div>
  );
}

