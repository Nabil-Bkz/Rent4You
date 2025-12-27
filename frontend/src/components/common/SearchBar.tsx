'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SearchBar() {
  const [lieu, setLieu] = useState('');
  const [date1, setDate1] = useState('');
  const [time1, setTime1] = useState('');
  const [date2, setDate2] = useState('');
  const [time2, setTime2] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (lieu) params.append('depot', lieu);
    if (date1) params.append('date_debut', date1);
    if (date2) params.append('date_fin', date2);
    router.push(`/visitor/search?${params.toString()}`);
  };

  return (
    <div className="search-bar" style={{
      background: '#fff',
      width: '100%',
      padding: '6px 10px 6px 30px',
      borderRadius: '0.5rem',
      border: '7px solid var(--orange)',
    }}>
      <form onSubmit={handleSearch} style={{
        display: 'grid',
        gridTemplateColumns: '30% 20% 8% 20% 8% 14%',
        gap: '6px 0',
        alignItems: 'center',
      }}>
        <input
          type="text"
          placeholder="Lieu"
          value={lieu}
          onChange={(e) => setLieu(e.target.value)}
          style={{
            width: '100%',
            padding: '1rem',
            fontSize: '1.6rem',
            background: 'transparent',
            borderRadius: '0.5rem',
          }}
        />
        <input
          type="date"
          value={date1}
          onChange={(e) => setDate1(e.target.value)}
          style={{
            width: '100%',
            padding: '1rem',
            fontSize: '1.6rem',
            background: 'transparent',
            borderRadius: '0.5rem',
          }}
        />
        <input
          type="time"
          value={time1}
          onChange={(e) => setTime1(e.target.value)}
          style={{
            width: '100%',
            padding: '1rem',
            fontSize: '1.6rem',
            background: 'transparent',
            borderRadius: '0.5rem',
          }}
        />
        <input
          type="date"
          value={date2}
          onChange={(e) => setDate2(e.target.value)}
          style={{
            width: '100%',
            padding: '1rem',
            fontSize: '1.6rem',
            background: 'transparent',
            borderRadius: '0.5rem',
          }}
        />
        <input
          type="time"
          value={time2}
          onChange={(e) => setTime2(e.target.value)}
          style={{
            width: '100%',
            padding: '1rem',
            fontSize: '1.6rem',
            background: 'transparent',
            borderRadius: '0.5rem',
          }}
        />
        <button
          type="submit"
          className="btn btn-primary"
          style={{ width: '100%' }}
        >
          Rechercher
        </button>
      </form>
    </div>
  );
}

