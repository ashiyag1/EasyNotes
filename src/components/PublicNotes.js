// src/components/PublicNotes.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './NotesGrid.css';

const PublicNotes = () => {
  const navigate = useNavigate();
  const notes = JSON.parse(localStorage.getItem('notes')) || [];
  const publicNotes = notes.filter((note) => note.isPublic);

  const openNote = (note) => {
    navigate('/editor', { state: { summary: note.text, title: note.title, images: note.images } });
  };

  return (
    <div className="notes-page">
      <h2>Public Notes</h2>
      {publicNotes.length > 0 ? (
        <div className="notes-grid">
          {publicNotes.map((note) => (
            <div className="note-card" key={note.id} onClick={() => openNote(note)}>
              <h3>{note.title}</h3>
              <p>{note.text.substring(0, 50)}...</p>
            </div>
          ))}
        </div>
      ) : (
        <p>No public notes available yet. Be the first to share one!</p>
      )}
    </div>
  );
};

export default PublicNotes;
