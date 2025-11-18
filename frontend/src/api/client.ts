export interface User {
    user_id: number
    username: string
    email: string
}

export interface Note {
    note_id: number
    user_id: number
    content: string
    created_at: string
    modified_at: string
}

const base = '/api'

export async function createUser(username: string, password: string, email: string): Promise<User> {
    const res = await fetch(`${base}/users?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&email=${encodeURIComponent(email)}`, {
        method: 'POST',
    })
    if (!res.ok) throw new Error(`Create user failed: ${res.status}`)
    return res.json()
}

export async function getUser(username: string): Promise<User> {
    const res = await fetch(`${base}/users/${encodeURIComponent(username)}`)
    if (!res.ok) throw new Error(`Get user failed: ${res.status}`)
    return res.json()
}

export async function getNotesByUserId(userId: number): Promise<Note[]> {
    const res = await fetch(`${base}/notes/user/${userId}`)
    if (res.status === 404) return []
    if (!res.ok) throw new Error(`Get notes failed: ${res.status}`)
    return res.json()
}

export async function addNote(userId: number, content: string): Promise<Note> {
    const res = await fetch(`${base}/notes?user_id=${userId}&content=${encodeURIComponent(content)}`, {
        method: 'POST',
    })
    if (!res.ok) throw new Error(`Add note failed: ${res.status}`)
    return res.json()
}

export async function updateNote(noteId: number, userId: number, content: string): Promise<Note> {
    const res = await fetch(`${base}/notes/${noteId}?user_id=${userId}&content=${encodeURIComponent(content)}`, {
        method: 'PUT',
    })
    if (!res.ok) throw new Error(`Update note failed: ${res.status}`)
    return res.json()
}