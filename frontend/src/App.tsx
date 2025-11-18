import { useEffect, useState } from 'react'
import './App.css'
import { addNote, createUser, getNotesByUserId, getUser, updateNote, type Note, type User } from './api/client'

function App() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [email, setEmail] = useState('')

  const [currentUser, setCurrentUser] = useState<User | null>(null)
  const [notes, setNotes] = useState<Note[]>([])
  const [newNote, setNewNote] = useState('')

  const [editingId, setEditingId] = useState<number | null>(null)
  const [editingContent, setEditingContent] = useState('')

  useEffect(() => {
    if (!currentUser) return
    refreshNotes(currentUser.user_id)
  }, [currentUser])

  async function refreshNotes(userId: number) {
    try {
      const data = await getNotesByUserId(userId)
      setNotes(data)
    } catch (e) {
      console.error(e)
      setNotes([])
    }
  }

  async function handleCreateUser() {
    try {
      const u = await createUser(username, password, email)
      setCurrentUser(u)
    } catch (e) {
      alert('Failed to create user. See console.')
      console.error(e)
    }
  }

  async function handleLoadUser() {
    try {
      const u = await getUser(username)
      setCurrentUser(u)
    } catch (e) {
      alert('User not found or error. See console.')
      console.error(e)
    }
  }

  async function handleAddNote() {
    if (!currentUser) return
    if (!newNote.trim()) return
    try {
      await addNote(currentUser.user_id, newNote.trim())
      setNewNote('')
      await refreshNotes(currentUser.user_id)
    } catch (e) {
      alert('Failed to add note. See console.')
      console.error(e)
    }
  }

  function startEdit(note: Note) {
    setEditingId(note.note_id)
    setEditingContent(note.content)
  }

  async function saveEdit(note: Note) {
    if (!currentUser) return
    try {
      await updateNote(note.note_id, currentUser.user_id, editingContent)
      setEditingId(null)
      setEditingContent('')
      await refreshNotes(currentUser.user_id)
    } catch (e) {
      alert('Failed to update note. See console.')
      console.error(e)
    }
  }

  return (
    <div>
      <h1>Notes App</h1>

      <section style={{ marginBottom: 24 }}>
        <h2>User</h2>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <input
            placeholder="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            placeholder="password (for create)"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <input
            placeholder="email (for create)"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button onClick={handleCreateUser}>Create User</button>
          <button onClick={handleLoadUser}>Load User</button>
        </div>

        {currentUser && (
          <p>
            Logged in as {currentUser.username} (id: {currentUser.user_id}, email: {currentUser.email})
          </p>
        )}
      </section>

      {currentUser && (
        <section>
          <h2>Notes</h2>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <input
              style={{ width: 320 }}
              placeholder="Write a new note..."
              value={newNote}
              onChange={(e) => setNewNote(e.target.value)}
            />
            <button onClick={handleAddNote}>Add Note</button>
          </div>

          <ul style={{ textAlign: 'left' }}>
            {notes.map((n) => (
              <li key={n.note_id} style={{ marginTop: 12 }}>
                {editingId === n.note_id ? (
                  <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    <input
                      style={{ width: 320 }}
                      value={editingContent}
                      onChange={(e) => setEditingContent(e.target.value)}
                    />
                    <button onClick={() => saveEdit(n)}>Save</button>
                    <button onClick={() => { setEditingId(null); setEditingContent('') }}>Cancel</button>
                  </div>
                ) : (
                  <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    <span>{n.content}</span>
                    <button onClick={() => startEdit(n)}>Edit</button>
                  </div>
                )}
                <div style={{ fontSize: 12, color: '#888' }}>
                  created: {n.created_at} | modified: {n.modified_at}
                </div>
              </li>
            ))}
            {notes.length === 0 && <li>No notes yet.</li>}
          </ul>
        </section>
      )}
    </div>
  )
}

export default App