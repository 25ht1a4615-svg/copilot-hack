// // create sveltekit server function to return data to page on load
// export async function load({ fetch }) {
//   const res = await fetch(`http://localhost:5000/predict?day_of_week=3&airport_id=14771`)
//   const result = await res.json()
//   console.log(result)
//   return result
// }

export async function load({ fetch }) {
  const res = await fetch(`http://localhost:5000/airports`);
  const airports = await res.json();
  // console.log({airports})
  return {airports};
}

export const actions = {
  getDelay: async ({fetch, request}) => {
    // get form data
    const data = await request.formData();

    const day_of_week = data.get('day');
    const airport_id = data.get('airport');

    // Validate inputs before making request
    if (!day_of_week || !airport_id) {
      return { error: 'Missing required fields' };
    }

    // Properly encode URL parameters to prevent injection
    const params = new URLSearchParams({
      day_of_week: String(day_of_week),
      airport_id: String(airport_id)
    });

    try {
      // make request to server
      const res = await fetch(`http://localhost:5000/predict?${params.toString()}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (!res.ok) {
        const errorData = await res.json();
        return { error: errorData.error || 'Prediction failed' };
      }
      
      const result = await res.json();
      return {result};
    } catch (err) {
      console.error('Fetch error:', err);
      return { error: 'Failed to fetch prediction' };
    }
  }
}