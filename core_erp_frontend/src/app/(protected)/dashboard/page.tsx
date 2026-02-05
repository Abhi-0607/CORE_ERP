'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function DashboardPage() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const router = useRouter()

  useEffect(() => {
    // Get token from localStorage
    const token = localStorage.getItem('token')
    
    // If no token, redirect to login
    if (!token) {
      router.push('/login')
      return
    }

    // Fetch dashboard data from backend
    fetch('http://localhost:8000/dashboard/', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
      .then(response => {
        if (response.status === 401) {
          // Token expired/invalid
          localStorage.removeItem('token')
          router.push('/login')
          return
        }
        return response.json()
      })
      .then(data => {
        setData(data)
      })
      .catch(err => {
        setError('Failed to load dashboard')
        console.error(err)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/login')
  }

  if (loading) {
    return (
      <div style={{ padding: '2rem' }}>
        Loading dashboard...
      </div>
    )
  }

  return (
    <div style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
        <h1>CORE ERP Dashboard</h1>
        <button onClick={handleLogout}>Logout</button>
      </div>
      
      {error ? (
        <div style={{ color: 'red' }}>{error}</div>
      ) : (
        <div style={{ 
          backgroundColor: 'white', 
          padding: '1.5rem',
          borderRadius: '8px',
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
        }}>
          <h2>Connected to Backend!</h2>
          
          {data && (
            <div style={{ marginTop: '1rem' }}>
              <h3>Dashboard Data:</h3>
              <pre style={{ 
                backgroundColor: '#f5f5f5', 
                padding: '1rem',
                borderRadius: '4px',
                overflow: 'auto',
                maxHeight: '400px'
              }}>
                {JSON.stringify(data, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  )
}