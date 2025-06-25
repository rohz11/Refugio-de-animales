export async function apiFetch(url, options) {
  const response = await fetch("http://localhost:5000" + url, options);
  if (!response.ok) {
    throw new Error("API request failed");
  }
  return response.json();
}
