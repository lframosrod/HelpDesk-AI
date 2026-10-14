const API_URL = "http://localhost:8080/api/v1";

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/documents/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) throw new Error("Error al subir el documento");
  return response.json();
}

export async function searchRAG(query: string) {
  const response = await fetch(`${API_URL}/documents/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, limit: 3 }),
  });

  if (!response.ok) throw new Error("Error en la búsqueda");
  return response.json();
}

export async function fetchArticles() {
  const response = await fetch(`${API_URL}/documents/articles`);
  if (!response.ok) throw new Error("Error al obtener los artículos");
  return response.json();
}
