/*
# Create chat sessions and messages tables

1. Purpose
This project is a web app that helps MEET Y1 students with two AI agents:
- CS instructor (Computer Science help)
- Entrepreneurship instructor (Entrepreneurship help)

The database stores the conversation history between students and each agent,
so conversations can be reviewed, resumed, and exported later.

2. New Tables

  a) `chat_sessions`
     - One row per conversation a student starts with an agent.
     - `id` (uuid, primary key)
     - `agent_mode` (text, not null): which agent the session uses.
       Allowed values: 'cs' or 'entrepreneurship'.
     - `title` (text, nullable): short label for the session, usually the
       first user message or a generated summary.
     - `created_at` (timestamptz, default now())
     - `updated_at` (timestamptz, default now()): touched when a new message
       is added, so sessions can be ordered by recent activity.

  b) `chat_messages`
     - One row per message inside a session (user or assistant).
     - `id` (uuid, primary key)
     - `session_id` (uuid, not null, foreign key to chat_sessions.id,
       ON DELETE CASCADE so deleting a session removes its messages)
     - `role` (text, not null): 'user' or 'assistant'
     - `content` (text, not null): the message text
     - `created_at` (timestamptz, default now())

3. Indexes
   - `chat_messages_session_id_idx` on chat_messages(session_id) for fast
     lookup of all messages in a session.
   - `chat_sessions_agent_mode_idx` on chat_sessions(agent_mode) for
     filtering sessions by agent.
   - `chat_sessions_updated_at_idx` on chat_sessions(updated_at DESC) for
     listing recent sessions.

4. Security
   - This is a single-tenant app with no sign-in screen, so all policies
     use `TO anon, authenticated` with `USING (true)` / `WITH CHECK (true)`
     because the data is intentionally shared/public.
   - RLS is enabled on both tables.
   - Four separate policies per table (SELECT, INSERT, UPDATE, DELETE).

5. Important Notes
   - The app reads and writes as the `anon` role for its entire lifetime.
   - No `user_id` column or `auth.uid()` checks because there is no auth.
   - Deleting a session automatically deletes its messages via CASCADE.
*/

CREATE TABLE IF NOT EXISTS chat_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_mode text NOT NULL CHECK (agent_mode IN ('cs', 'entrepreneurship')),
  title text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS chat_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id uuid NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
  role text NOT NULL CHECK (role IN ('user', 'assistant')),
  content text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS chat_messages_session_id_idx
  ON chat_messages(session_id);

CREATE INDEX IF NOT EXISTS chat_sessions_agent_mode_idx
  ON chat_sessions(agent_mode);

CREATE INDEX IF NOT EXISTS chat_sessions_updated_at_idx
  ON chat_sessions(updated_at DESC);

ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

-- chat_sessions policies (single-tenant, public/shared data)
DROP POLICY IF EXISTS "anon_select_chat_sessions" ON chat_sessions;
CREATE POLICY "anon_select_chat_sessions" ON chat_sessions FOR SELECT
  TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "anon_insert_chat_sessions" ON chat_sessions;
CREATE POLICY "anon_insert_chat_sessions" ON chat_sessions FOR INSERT
  TO anon, authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "anon_update_chat_sessions" ON chat_sessions;
CREATE POLICY "anon_update_chat_sessions" ON chat_sessions FOR UPDATE
  TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "anon_delete_chat_sessions" ON chat_sessions;
CREATE POLICY "anon_delete_chat_sessions" ON chat_sessions FOR DELETE
  TO anon, authenticated USING (true);

-- chat_messages policies (single-tenant, public/shared data)
DROP POLICY IF EXISTS "anon_select_chat_messages" ON chat_messages;
CREATE POLICY "anon_select_chat_messages" ON chat_messages FOR SELECT
  TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "anon_insert_chat_messages" ON chat_messages;
CREATE POLICY "anon_insert_chat_messages" ON chat_messages FOR INSERT
  TO anon, authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "anon_update_chat_messages" ON chat_messages;
CREATE POLICY "anon_update_chat_messages" ON chat_messages FOR UPDATE
  TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "anon_delete_chat_messages" ON chat_messages;
CREATE POLICY "anon_delete_chat_messages" ON chat_messages FOR DELETE
  TO anon, authenticated USING (true);
