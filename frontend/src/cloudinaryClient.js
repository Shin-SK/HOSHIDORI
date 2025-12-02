// frontend/src/cloudinaryClient.js
const cloudName = import.meta.env.VITE_CLOUDINARY_CLOUD_NAME
const uploadPreset = import.meta.env.VITE_CLOUDINARY_UPLOAD_PRESET

export async function uploadImage(file) {
  if (!cloudName || !uploadPreset) {
    throw new Error('Cloudinary env not set')
  }

  const endpoint = `https://api.cloudinary.com/v1_1/${cloudName}/upload`
  const formData = new FormData()
  formData.append('file', file)
  formData.append('upload_preset', uploadPreset)

  const res = await fetch(endpoint, {
    method: 'POST',
    body: formData,
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Cloudinary upload error: ${text}`)
  }

  const data = await res.json()
  // data.secure_url が最終的な画像URL
  return data.secure_url
}