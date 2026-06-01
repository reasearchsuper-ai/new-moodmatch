import Anthropic from '@anthropic-ai/sdk'
import type { Context } from '@netlify/functions'

const anthropic = new Anthropic()

const PROMPT = `Analyze the facial expressions visible in this image and return emotion scores.

Return ONLY a valid JSON object with this exact structure (no markdown, no explanation):
{
  "dominant": "happy",
  "scores": {
    "happy": 0,
    "sad": 0,
    "angry": 0,
    "surprised": 0,
    "fearful": 0,
    "disgusted": 0,
    "neutral": 0
  },
  "confidence": 0
}

Rules:
- All score values are integers 0–100 and must sum to exactly 100
- dominant is the key with the highest score
- confidence is the dominant score (0–100)
- If no face is visible, set neutral to 100 and dominant to "neutral"
- Return ONLY valid JSON, nothing else`

export default async (req: Request, context: Context) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    })
  }

  if (req.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 })
  }

  try {
    const body = await req.json()
    const { imageBase64, mimeType = 'image/jpeg' } = body

    if (!imageBase64) {
      return Response.json({ error: 'No image provided' }, { status: 400 })
    }

    const validMimeTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'] as const
    const safeType = validMimeTypes.includes(mimeType as typeof validMimeTypes[number])
      ? (mimeType as typeof validMimeTypes[number])
      : 'image/jpeg'

    const message = await anthropic.messages.create({
      model: 'claude-haiku-4-5',
      max_tokens: 256,
      messages: [
        {
          role: 'user',
          content: [
            {
              type: 'image',
              source: {
                type: 'base64',
                media_type: safeType,
                data: imageBase64,
              },
            },
            {
              type: 'text',
              text: PROMPT,
            },
          ],
        },
      ],
    })

    const text = message.content[0].type === 'text' ? message.content[0].text.trim() : '{}'

    let result
    try {
      result = JSON.parse(text)
    } catch {
      // If parsing fails, default to neutral
      result = {
        dominant: 'neutral',
        scores: { happy: 0, sad: 0, angry: 0, surprised: 0, fearful: 0, disgusted: 0, neutral: 100 },
        confidence: 100,
      }
    }

    return Response.json(result, {
      headers: { 'Access-Control-Allow-Origin': '*' },
    })
  } catch (err) {
    console.error('Emotion analysis error:', err)
    return Response.json({ error: 'Analysis failed' }, { status: 500 })
  }
}

export const config = {
  path: '/api/analyze-emotion',
}
