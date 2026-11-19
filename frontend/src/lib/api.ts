import { z } from "zod";

export async function loadCampaigns() {
  return sendApiRequest({ method: "GET", path: "/campaigns", schema: z.array(CAMPAIGN_SCHEMA) });
}

export async function createCampaign(form: CampaignForm) {
  return sendApiRequest({ method: "POST", path: "/campaigns", body: form, schema: CAMPAIGN_SCHEMA });
}

export interface CampaignForm {
  name: string;
  country: string;
  offer_id: Offer["id"];
  domain_id: Domain["id"];
  group_id: CampaignGroup["id"];
  traffic_source_id: TrafficSource["id"];
}

export async function loadOffers() {
  return sendApiRequest({ method: "GET", path: "/offers", schema: z.array(OFFER_SCHEMA) });
}

export async function loadDomains() {
  return sendApiRequest({ method: "GET", path: "/domains", schema: z.array(DOMAIN_SCHEMA) });
}

export async function loadCampaignGroups() {
  return sendApiRequest({ method: "GET", path: "/campaign-groups", schema: z.array(CAMPAIGN_GROUP_SCHEMA) });
}

export async function loadTrafficSources() {
  return sendApiRequest({ method: "GET", path: "/traffic-sources", schema: z.array(TRAFFIC_SOURCE_SCHEMA) });
}

export async function loadCampaignOffers(campaignId: Campaign["id"]) {
  const path = getCampaignOffersPath(campaignId);
  return sendApiRequest({ method: "GET", path, schema: z.array(STREAM_OFFER_SCHEMA) });
}

export async function addCampaignOffer(campaignId: Campaign["id"], offerId: Offer["id"]) {
  const path = getCampaignOfferPath(campaignId, offerId);
  return sendApiRequest({ method: "POST", path, schema: z.array(STREAM_OFFER_SCHEMA) });
}

export async function removeCampaignOffer(campaignId: Campaign["id"], offerId: Offer["id"]) {
  const path = getCampaignOfferPath(campaignId, offerId);
  return sendApiRequest({ method: "DELETE", path, schema: z.array(STREAM_OFFER_SCHEMA) });
}

export function describeApiRejection(error: unknown): string | undefined {
  if (!(error instanceof ApiRequestRejectedError)) return;
  return convertApiRejectionDetailToText(error.detail);
}

async function sendApiRequest<Schema extends z.ZodType>(request: ApiRequest<Schema>): Promise<z.output<Schema>> {
  const response = await fetchApiResponse(request);
  if (!response.ok) throw await readApiRequestRejectionError(request, response);
  const body = await readApiResponseBody(request, response);
  return parseApiResponseBody(body, request);
}

interface ApiRequest<Schema extends z.ZodType> {
  method: "GET" | "POST" | "DELETE";
  path: string;
  body?: unknown;
  schema: Schema;
}

function getCampaignOffersPath(campaignId: Campaign["id"]) {
  return `/campaigns/${campaignId}/offers`;
}

function getCampaignOfferPath(campaignId: Campaign["id"], offerId: Offer["id"]) {
  return `${getCampaignOffersPath(campaignId)}/${offerId}`;
}

function convertApiRejectionDetailToText(detail: unknown): string | undefined {
  if (detail === undefined || typeof detail === "string") return detail;
  return JSON.stringify(detail);
}

async function fetchApiResponse(request: ApiRequest<z.ZodType>) {
  try {
    return await fetch(`${API_PATH}${request.path}`, convertApiRequestToFetchOptions(request));
  } catch (error) {
    throw new ApiRequestFailedError({ request, cause: error });
  }
}

async function readApiRequestRejectionError(request: ApiRequest<z.ZodType>, response: Response) {
  const detail = await readApiRejectionDetail(response);
  return new ApiRequestRejectedError({ request, status: response.status, detail });
}

async function readApiResponseBody(request: ApiRequest<z.ZodType>, response: Response): Promise<unknown> {
  try {
    return await response.json();
  } catch (error) {
    throw new ApiRequestFailedError({ request, cause: error });
  }
}

function parseApiResponseBody<Schema extends z.ZodType>(body: unknown, request: ApiRequest<Schema>): z.output<Schema> {
  const parsed = request.schema.safeParse(body);
  if (!parsed.success) throw new ApiRequestFailedError({ request, cause: parsed.error });
  return parsed.data;
}

function convertApiRequestToFetchOptions(request: ApiRequest<z.ZodType>): RequestInit {
  if (request.body === undefined) return { method: request.method };

  return {
    method: request.method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request.body),
  };
}

async function readApiRejectionDetail(response: Response): Promise<unknown> {
  const body: unknown = await response.json().catch(() => undefined);
  const parsed = API_REJECTION_BODY_SCHEMA.safeParse(body);
  return parsed.data?.detail;
}

export class ApiRequestFailedError extends Error {
  public name = ApiRequestFailedError.name;
  public method: ApiRequest<z.ZodType>["method"];
  public path: string;

  public constructor(options: ErrorOptions & { request: ApiRequest<z.ZodType>; message?: string }) {
    super(options.message ?? `Request ${options.request.method} ${options.request.path} failed`, options);
    this.method = options.request.method;
    this.path = options.request.path;
  }
}

export class ApiRequestRejectedError extends ApiRequestFailedError {
  public name = ApiRequestRejectedError.name;
  public status: number;
  public detail: unknown;

  public constructor(
    options: ErrorOptions & { request: ApiRequest<z.ZodType>; status: number; detail: unknown },
  ) {
    super({
      ...options,
      message: `Request ${options.request.method} ${options.request.path} was rejected with ${options.status}: ${JSON.stringify(options.detail)}`,
    });

    this.status = options.status;
    this.detail = options.detail;
  }
}

const API_PATH = "/api";

const NAMED_RECORD_SCHEMA = z.object({ id: z.number(), name: z.string() });

const CAMPAIGN_SCHEMA = NAMED_RECORD_SCHEMA;
export type Campaign = z.output<typeof CAMPAIGN_SCHEMA>;

const OFFER_SCHEMA = NAMED_RECORD_SCHEMA;
export type Offer = z.output<typeof OFFER_SCHEMA>;

const DOMAIN_SCHEMA = NAMED_RECORD_SCHEMA;
export type Domain = z.output<typeof DOMAIN_SCHEMA>;

const CAMPAIGN_GROUP_SCHEMA = NAMED_RECORD_SCHEMA;
export type CampaignGroup = z.output<typeof CAMPAIGN_GROUP_SCHEMA>;

const TRAFFIC_SOURCE_SCHEMA = NAMED_RECORD_SCHEMA;
export type TrafficSource = z.output<typeof TRAFFIC_SOURCE_SCHEMA>;

export type NamedRecord = z.output<typeof NAMED_RECORD_SCHEMA>;

const STREAM_OFFER_SCHEMA = z.object({
  offer_id: z.number(),
  share: z.number(),
  state: z.enum(["active", "disabled"]),
});

export type StreamOffer = z.output<typeof STREAM_OFFER_SCHEMA>;

const API_REJECTION_BODY_SCHEMA = z.object({ detail: z.unknown() });
