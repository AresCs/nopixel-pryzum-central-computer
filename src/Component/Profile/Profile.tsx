import React from 'react';
import { ProfileData } from '../../App';
import './Profile.css';
import Placeholder from './NoTargetFound.png';

interface ProfileProps {
  profileData: ProfileData;
}

const Profile: React.FC<ProfileProps> = ({ profileData }) => {
  const profileImageUrl = profileData['Picture of Person'] || Placeholder;

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h3>{profileData.Name}</h3>
        <div className="window-controls">
          &#x2013; {/* Minimize */}
          &#x2610; {/* Fullscreen */}
          &#x2715; {/* Close */}
        </div>
      </div>
      <div className="profile-content">
        <img 
          src={profileImageUrl} 
          alt={`Profile of ${profileData.Name}`} 
          onError={(e) => {
            console.error("Image failed to load:", e.currentTarget.src);
            e.currentTarget.src = Placeholder;
          }} 
        />
        <div className="profile-details">
        <p><strong>State ID</strong> {profileData['State ID']}</p>
          <p><strong>Phone Number:</strong> {profileData["Phone Number"]}</p>
          <p><strong>Gang/Association:</strong> {profileData["Gang/Association"]}</p>
          <p><strong>Nicknames:</strong> {profileData.Nicknames}</p>
          <p><strong>Dirt:</strong> {profileData.Dirt}</p>
          <p><strong>Information:</strong> {profileData.Information}</p>
          <p><strong>Properties:</strong> {profileData.Properties}</p>
          <p><strong>Occupations:</strong> {profileData.Occupations}</p>
        </div>
      </div>
    </div>
  );
};

export default Profile;
