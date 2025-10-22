async function fecthHealthCheck() {
    // Make an API call to the health check endpoint
    const url = 'http://localhost:8000/health/';
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        const result = await response.json();
        console.log(result);

    } catch (error) {
        console.error(error.message);
    }
}

export { fecthHealthCheck };