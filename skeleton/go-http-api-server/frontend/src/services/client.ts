export interface Request {
	toBody(): string;
}

export class HttpClient {
	private baseUrl: string;

	constructor() {
		this.baseUrl = import.meta.env.VITE_API_BASE_URL as string;
	}

	async get(url: string): Promise<Response> {
		const response = await fetch(this.baseUrl + url);
		return response;
	}

	async post<T extends Request>(url: string, data: T): Promise<Response> {
		const response = await fetch(this.baseUrl + url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: data.toBody(),
		});
		return response;
	}
}
