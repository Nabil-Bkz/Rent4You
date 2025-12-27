'use client';

import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { useState } from 'react';

export default function Navbar() {
  const { user, isAuthenticated, logout, hasRole } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  const getDashboardLink = () => {
    if (!user) return '/login';
    const role = user.role;
    if (role === 'ADMIN') return '/admin';
    if (role === 'OWNER') return '/owner';
    if (role === 'SECRETARY') return '/secretary';
    if (role === 'MECHANIC') return '/mechanic';
    if (role === 'RENTER') return '/renter';
    if (role === 'AGENCY_ADMIN') return '/agency-admin';
    return '/visitor';
  };

  return (
    <header className="header" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 1000,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '2rem 9%',
      background: '#fff',
      boxShadow: 'var(--box-shadow)',
      height: '60px',
    }}>
      <Link href="/" className="logo" style={{
        fontSize: '2.5rem',
        fontWeight: 'bold',
        color: 'var(--black)',
      }}>
        <i style={{ color: 'var(--orange)' }}>🚗</i> Rent4You
      </Link>

      <nav className="navbar" style={{
        display: menuOpen ? 'flex' : 'none',
        flexDirection: menuOpen ? 'column' : 'row',
        position: menuOpen ? 'absolute' : 'static',
        top: menuOpen ? '100%' : 'auto',
        right: menuOpen ? '2rem' : 'auto',
        background: menuOpen ? '#fff' : 'transparent',
        boxShadow: menuOpen ? 'var(--box-shadow)' : 'none',
        borderRadius: menuOpen ? '0.5rem' : '0',
        padding: menuOpen ? '2rem' : '0',
        width: menuOpen ? '30rem' : 'auto',
      }}>
        <Link href="/visitor" style={{ fontSize: '1.7rem', margin: '0 1rem', color: 'var(--black)' }}>
          Véhicules
        </Link>
        {isAuthenticated ? (
          <>
            <Link href={getDashboardLink()} style={{ fontSize: '1.7rem', margin: '0 1rem', color: 'var(--black)' }}>
              Tableau de bord
            </Link>
            <Link href="/profile" style={{ fontSize: '1.7rem', margin: '0 1rem', color: 'var(--black)' }}>
              Profil
            </Link>
            <button
              onClick={logout}
              style={{
                fontSize: '1.7rem',
                margin: '0 1rem',
                color: 'var(--black)',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              Déconnexion
            </button>
          </>
        ) : (
          <>
            <Link href="/login" style={{ fontSize: '1.7rem', margin: '0 1rem', color: 'var(--black)' }}>
              Connexion
            </Link>
            <Link href="/register" style={{ fontSize: '1.7rem', margin: '0 1rem', color: 'var(--black)' }}>
              Inscription
            </Link>
          </>
        )}
      </nav>

      <button
        id="menu-btn"
        onClick={() => setMenuOpen(!menuOpen)}
        style={{
          display: 'none',
          fontSize: '2rem',
          cursor: 'pointer',
          background: '#eee',
          padding: '1rem',
          borderRadius: '0.5rem',
        }}
      >
        ☰
      </button>
    </header>
  );
}

