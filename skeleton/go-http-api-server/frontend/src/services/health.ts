import { HttpClient } from "./client";

const httpClient = new HttpClient();

const getHealth = async () => {
	try {
		const response = await httpClient.get("/api/health");
		return response.text();
	} catch (error) {
		console.error("Error fetching health data:", error);
		throw error;
	}
};

export { getHealth };
