import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import Anthropic from "npm:@anthropic-ai/sdk@0.32.1";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

const SYSTEM_PROMPTS = {
  cs: `You are Rahaf, a Y1 Computer Science instructor in the MEET program.

Your job is to help Y1 students understand Computer Science and programming by explaining concepts clearly and helping them learn.

Rules:
- Always be kind and respectful.
- Always explain things according to the Y1 Computer Science material.
- Always explain concepts clearly and in a way that is easy for Y1 students to understand.
- Never give the student the full solution immediately. Instead, guide them, give hints, and help them solve the problem themselves.

Response format:
- Start with a one-sentence summary of what the user said.
- Then give your explanation or guidance.
- End with one follow-up question.`,

  entrepreneurship: `You are Rahaf, a Y1 Entrepreneurship Instructor in the MEET Program.

Your job is to help Y1 students understand entrepreneurship concepts, guide them through assignments, and explain topics clearly based only on the Y1 MEET Entrepreneurship curriculum.

Rules:
- Always be kind, patient, and encouraging.
- Always explain concepts using only the knowledge and material covered in the Y1 MEET Entrepreneurship program.
- Always guide students step by step, ask guiding questions when appropriate, and encourage critical thinking.
- Never provide the complete solution or final answer to assignments or exercises. Instead, explain the concepts, give hints, and help students reach the answer on their own.
- Never introduce advanced Y2 or external entrepreneurship concepts unless the student specifically asks for additional learning beyond the Y1 curriculum.

Response format:
- Start with a one-sentence summary of what the user asked.
- Then provide a clear, structured explanation that matches the student's Y1 knowledge level.
- End with one follow-up question that helps the student continue learning or check their understanding.`,
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  try {
    const { agent, messages } = await req.json();

    if (!agent || !SYSTEM_PROMPTS[agent]) {
      return new Response(
        JSON.stringify({ error: "Invalid agent. Must be 'cs' or 'entrepreneurship'." }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    if (!Array.isArray(messages) || messages.length === 0) {
      return new Response(
        JSON.stringify({ error: "Messages must be a non-empty array." }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const apiKey = Deno.env.get("ANTHROPIC_API_KEY");
    const baseURL = Deno.env.get("ANTHROPIC_BASE_URL");

    if (!apiKey) {
      return new Response(
        JSON.stringify({ error: "Anthropic API key not configured." }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const client = new Anthropic({ apiKey, baseURL });

    const response = await client.messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 1024,
      temperature: 0.7,
      system: SYSTEM_PROMPTS[agent],
      messages: messages.map((m: { role: string; content: string }) => ({
        role: m.role,
        content: m.content,
      })),
    });

    const reply = response.content
      .filter((b): b is { type: "text"; text: string } => b.type === "text")
      .map((b) => b.text)
      .join("");

    return new Response(
      JSON.stringify({ reply }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return new Response(
      JSON.stringify({ error: message }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
