'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const { isAuthenticated, user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (isAuthenticated) {
        // Redirect based on role
        const role = user?.role;
        if (role === 'ADMIN') router.push('/admin');
        else if (role === 'OWNER') router.push('/owner');
        else if (role === 'SECRETARY') router.push('/secretary');
        else if (role === 'MECHANIC') router.push('/mechanic');
        else if (role === 'RENTER') router.push('/renter');
        else if (role === 'AGENCY_ADMIN') router.push('/agency-admin');
        else router.push('/visitor');
      } else {
        router.push('/visitor');
      }
    }
  }, [isAuthenticated, loading, user, router]);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <p>Chargement...</p>
      </div>
    );
  }

  return null;
}

