'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { authAPI } from '@/lib/api/auth';
import { agenciesAPI } from '@/lib/api/agencies';
import Navbar from '@/components/common/Navbar';
import Button from '@/components/common/Button';

export default function AdminDashboard() {
  const { isAuthenticated, user, hasRole, loading: authLoading } = useAuth();
  const router = useRouter();
  const [partnerships, setPartnerships] = useState<any[]>([]);
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    if (!authLoading) {
      if (!isAuthenticated || !hasRole('ADMIN')) {
        router.push('/login');
      } else {
        loadData();
      }
    }
  }, [isAuthenticated, authLoading, hasRole, router]);

  const loadData = async () => {
    try {
      // Load partnership requests
      const partnershipsData = await agenciesAPI.getAll();
      setPartnerships(partnershipsData);
      
      // Load users (would need a users API endpoint)
      // const usersData = await usersAPI.getAll();
      // setUsers(usersData);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const handleApprovePartnership = async (id: number) => {
    try {
      await agenciesAPI.approvePartnership(id);
      loadData();
      alert('Demande de partenariat approuvée');
    } catch (error) {
      alert('Erreur lors de l\'approbation');
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
            Tableau de bord <span>Administrateur</span>
          </h1>

          <div style={{ marginBottom: '3rem' }}>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '1.5rem' }}>Demandes de Partenariat</h2>
            {partnerships.length === 0 ? (
              <p>Aucune demande</p>
            ) : (
              <div style={{ display: 'grid', gap: '1rem' }}>
                {partnerships.map((partnership: any) => (
                  <div key={partnership.id} className="card">
                    <h3>{partnership.nom_agence}</h3>
                    <p>Email: {partnership.email_agence}</p>
                    <p>Statut: {partnership.status}</p>
                    {partnership.status === 'PENDING' && (
                      <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                        <Button onClick={() => handleApprovePartnership(partnership.id)}>
                          Approuver
                        </Button>
                        <Button variant="secondary" onClick={() => agenciesAPI.rejectPartnership(partnership.id)}>
                          Rejeter
                        </Button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          <div>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '1.5rem' }}>Gestion des Utilisateurs</h2>
            <p>Fonctionnalité à implémenter</p>
          </div>
        </section>
      </div>
    </>
  );
}

