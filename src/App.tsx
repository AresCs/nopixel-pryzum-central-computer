import React, { useState, useEffect } from 'react';
import Profile from './Component/Profile/Profile';
import SearchBar from './Component/SearchBar/SearchBar';
import Login from './Component/Login/Login';
import './App.css';
import Logo from './Component/Logos/Pryzym_Logo2.png';
import { decryptData } from './utils/decrypt';
import bcrypt from 'bcryptjs';

// URLs for your encrypted data
const encryptedDataUrl = '/secure/pryzumData.json';
const encryptedLoginsUrl = '/secure/Logins.enc';

export interface ProfileData {
  Name: string;
  "State ID": number;
  "Phone Number": number;
  "Gang/Association": string;
  Nicknames: string;
  "Date of Birth": string;
  Dirt: string | null;
  Properties: string | null;
  Information: string | null;
  Occupations: string;
  "Picture of Person": string | null;
  "Date of Entry": string;
}

interface LoginCredentials {
  username: string;
  password: string; // This should be a hashed password
}

const App = () => {
  const [profiles, setProfiles] = useState<ProfileData[]>([]);
  const [searchResults, setSearchResults] = useState<ProfileData[]>([]);
  const [searchIndex, setSearchIndex] = useState(0);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loginData, setLoginData] = useState<LoginCredentials[]>([]);

  useEffect(() => {
    // Fetch the key and encrypted data
    Promise.all([
      fetch('/secure/key.key').then(response => response.text()),
      fetch(encryptedDataUrl).then(response => response.text()),
      fetch(encryptedLoginsUrl).then(response => response.text())
    ]).then(([key, encryptedData, encryptedLogins]) => {
      const decryptedProfiles = decryptData(encryptedData, key.trim());
      const decryptedLogins = decryptData(encryptedLogins, key.trim());
      setProfiles(decryptedProfiles.pryzumData);
      setSearchResults(decryptedProfiles.pryzumData);
      setLoginData(decryptedLogins);
    }).catch(error => {
      console.error('Error fetching or decrypting data:', error);
    });
  }, []);

  const handleSearch = (query: string) => {
    if (!query) {
      setSearchResults(profiles);
      setSearchIndex(0);
    } else {
      const filteredProfiles = profiles.filter(profile =>
        profile.Name.toLowerCase().includes(query.toLowerCase())
      );
      setSearchResults(filteredProfiles);
      setSearchIndex(0);
    }
  };

  const handleNext = () => {
    if (searchIndex < searchResults.length - 1) {
      setSearchIndex(prevIndex => prevIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (searchIndex > 0) {
      setSearchIndex(prevIndex => prevIndex - 1);
    }
  };

  const handleLogin = (username: string, password: string) => {
    const user = loginData.find((user: LoginCredentials) => user.username === username);

    if (user) {
      bcrypt.compare(password, user.password, (err, result) => {
        if (result) {
          setIsLoggedIn(true);
        } else {
          alert('Invalid credentials');
        }
      });
    } else {
      alert('Invalid credentials');
    }
  };

  if (!isLoggedIn) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <img src={Logo} className="app-logo" alt="Pryzum Logo" />
        <SearchBar onSearch={handleSearch} />
        <div className="button-container">
          <button onClick={handlePrevious} disabled={searchIndex === 0}>Previous</button>
          <button onClick={handleNext} disabled={searchIndex === searchResults.length - 1}>Next</button>
        </div>
      </header>
      <div className="profile-container">
        {searchResults.length > 0 ? (
          <Profile profileData={searchResults[searchIndex]} />
        ) : (
          <p>No profiles found</p>
        )}
      </div>
      <div className="noise"></div>
      <div className="lines"></div>
    </div>
  );
};

export default App;
