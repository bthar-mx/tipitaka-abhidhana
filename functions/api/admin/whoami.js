// GET /api/admin/whoami — {email} when the Access token verifies (the _middleware checked it).
import { json } from '../../_lib/edits.js';
export const onRequestGet = ({ data }) => json({ email: data.editor.email });
