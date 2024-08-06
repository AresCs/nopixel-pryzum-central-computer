import React, { useState, useEffect } from 'react';
import Profile from './Component/Profile/Profile';
import SearchBar from './Component/SearchBar/SearchBar';
import Login from './Component/Login/Login';
import './App.css';
import Logo from './Component/Logos/Pryzym_Logo2.png';
import loginData from './Component/Login/Logins.json';
import profileData from './data/pryzumData.json';

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
  password: string;
}

const App = () => {
  const [profiles, setProfiles] = useState<ProfileData[]>([]);
  const [searchResults, setSearchResults] = useState<ProfileData[]>([]);
  const [searchIndex, setSearchIndex] = useState(0);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Initialize profiles with data from the JSON file
    setProfiles(profileData.pryzumData);
    setSearchResults(profileData.pryzumData);
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
    const user = loginData.find((user: LoginCredentials) => user.username === username && user.password === password);
    if (user) {
      setIsLoggedIn(true);
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
      </header>
      <div className="profile-container">
        {searchResults.length > 0 ? (
          <Profile profileData={searchResults[searchIndex]} />
        ) : (
          <p>No profiles found</p>
        )}
        <button onClick={handlePrevious} disabled={searchIndex === 0}>
          Previous
        </button>
        <button onClick={handleNext} disabled={searchIndex === searchResults.length - 1}>
          Next
        </button>
      </div>
      <div className="noise"></div>
      <div className="lines"></div>
    </div>
  );
};

export default App;
