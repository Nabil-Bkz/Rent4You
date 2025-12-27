'use client';

import { useEffect, useState } from 'react';
import { vehiclesAPI, Vehicle } from '@/lib/api/vehicles';
import VehicleCard from '@/components/common/VehicleCard';
import SearchBar from '@/components/common/SearchBar';
import Navbar from '@/components/common/Navbar';

export default function VisitorPage() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadVehicles();
  }, []);

  const loadVehicles = async () => {
    try {
      const data = await vehiclesAPI.getAll({ disponibilite: true });
      setVehicles(data);
    } catch (error) {
      console.error('Error loading vehicles:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />
      <div style={{ paddingTop: '80px' }}>
        <section className="home" style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'url(/image/range2.avif) no-repeat',
          backgroundPosition: 'center',
          backgroundSize: 'cover',
          paddingTop: '17rem',
          paddingBottom: '10rem',
          height: '600px',
        }}>
          <div style={{ textAlign: 'center', width: '160rem' }}>
            <h3 style={{ color: '#fff', fontSize: '3rem' }}>
              Trouver, réserver et louer<br />
              des véhicules en quelques étapes <span style={{ color: 'var(--orange)' }}>simples</span>
            </h3>
          </div>
        </section>

        <section style={{ padding: '2rem 9%' }}>
          <SearchBar />
        </section>

        <section style={{ padding: '2rem 9%' }}>
          <h2 className="heading">
            Nos <span>Véhicules</span>
          </h2>
          
          {loading ? (
            <p style={{ textAlign: 'center' }}>Chargement...</p>
          ) : (
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(30rem, 1fr))',
              gap: '1.5rem',
            }}>
              {vehicles.map((vehicle) => (
                <VehicleCard key={vehicle.id} vehicle={vehicle} />
              ))}
            </div>
          )}
        </section>
      </div>
    </>
  );
}

