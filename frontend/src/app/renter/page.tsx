'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { vehiclesAPI, Vehicle } from '@/lib/api/vehicles';
import { reservationsAPI, Reservation } from '@/lib/api/reservations';
import Navbar from '@/components/common/Navbar';
import VehicleCard from '@/components/common/VehicleCard';
import Modal from '@/components/common/Modal';
import Button from '@/components/common/Button';

export default function RenterDashboard() {
  const { isAuthenticated, user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [showReservationModal, setShowReservationModal] = useState(false);
  const [selectedVehicle, setSelectedVehicle] = useState<Vehicle | null>(null);
  const [reservationData, setReservationData] = useState({
    date_debut: '',
    date_fin: '',
    code_promo: '',
  });

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  useEffect(() => {
    if (isAuthenticated) {
      loadVehicles();
      loadReservations();
    }
  }, [isAuthenticated]);

  const loadVehicles = async () => {
    try {
      const data = await vehiclesAPI.getAll({ disponibilite: true });
      setVehicles(data);
    } catch (error) {
      console.error('Error loading vehicles:', error);
    }
  };

  const loadReservations = async () => {
    try {
      const data = await reservationsAPI.getAll();
      setReservations(data);
    } catch (error) {
      console.error('Error loading reservations:', error);
    }
  };

  const handleReserve = (vehicle: Vehicle) => {
    setSelectedVehicle(vehicle);
    setShowReservationModal(true);
  };

  const submitReservation = async () => {
    if (!selectedVehicle) return;
    try {
      await reservationsAPI.create({
        date_debut: reservationData.date_debut,
        date_fin: reservationData.date_fin,
        vehicule: selectedVehicle.id,
        code_promo: reservationData.code_promo || undefined,
      });
      setShowReservationModal(false);
      loadReservations();
      alert('Réservation créée avec succès!');
    } catch (error: any) {
      alert(error.response?.data?.error || 'Erreur lors de la réservation');
    }
  };

  if (authLoading) {
    return <div style={{ textAlign: 'center', padding: '2rem' }}>Chargement...</div>;
  }

  return (
    <>
      <Navbar />
      <div style={{ paddingTop: '80px', minHeight: '100vh' }}>
        <section style={{ padding: '2rem 9%' }}>
          <h1 className="heading">
            Tableau de bord <span>Locataire</span>
          </h1>

          <div style={{ marginBottom: '3rem' }}>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '1.5rem' }}>Mes Réservations</h2>
            {reservations.length === 0 ? (
              <p>Aucune réservation</p>
            ) : (
              <div style={{ display: 'grid', gap: '1rem' }}>
                {reservations.map((res) => (
                  <div key={res.id} className="card">
                    <h3>{res.vehicule_details?.marque} {res.vehicule_details?.model}</h3>
                    <p>Du {new Date(res.date_debut).toLocaleDateString()} au {new Date(res.date_fin).toLocaleDateString()}</p>
                    <p>Prix: {res.prix}€</p>
                    <p>Statut: {res.status}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '1.5rem' }}>Véhicules Disponibles</h2>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(30rem, 1fr))',
              gap: '1.5rem',
            }}>
              {vehicles.map((vehicle) => (
                <div key={vehicle.id}>
                  <VehicleCard vehicle={vehicle} />
                  <Button onClick={() => handleReserve(vehicle)} style={{ width: '100%' }}>
                    Réserver
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>

      <Modal
        isOpen={showReservationModal}
        onClose={() => setShowReservationModal(false)}
        title="Nouvelle Réservation"
      >
        {selectedVehicle && (
          <>
            <p><strong>{selectedVehicle.marque} {selectedVehicle.model}</strong></p>
            <div className="form-group">
              <label>Date de début</label>
              <input
                type="date"
                value={reservationData.date_debut}
                onChange={(e) => setReservationData({ ...reservationData, date_debut: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Date de fin</label>
              <input
                type="date"
                value={reservationData.date_fin}
                onChange={(e) => setReservationData({ ...reservationData, date_fin: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Code promo (optionnel)</label>
              <input
                type="text"
                value={reservationData.code_promo}
                onChange={(e) => setReservationData({ ...reservationData, code_promo: e.target.value })}
              />
            </div>
            <Button onClick={submitReservation}>Confirmer</Button>
          </>
        )}
      </Modal>
    </>
  );
}

