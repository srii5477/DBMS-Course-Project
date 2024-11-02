DROP TABLE IF EXISTS Disaster, Locality, Funding_Source, Essential, Organization, Volunteer,
Shelter, Emergency_Service, Incident, Incident_Funding, Incident_Resource_Allocation, Incident_Volunteer_Allotment ;

CREATE TABLE "disaster" (
  "id" integer PRIMARY KEY,
  "name" text,
  "description" text,
  "protocol" text
);

CREATE TABLE "locality" (
  "id" integer PRIMARY KEY,
  "name" text,
  "geographical_size" text,
  "development_level" text
);

CREATE TABLE "funding_source" (
  "id" integer PRIMARY KEY,
  "name" text,
  "contract_terms" text,
  "renewal_period" integer,
  "std_amt_donated" integer,
  "contact" text,
  "type_of_organization" text
);

CREATE TABLE "essential" (
  "id" integer PRIMARY KEY,
  "name" text,
  "price_per_unit" integer,
  "qty_in_stock" integer
);

CREATE TABLE "organization" (
  "id" integer PRIMARY KEY,
  "name" text,
  "type_of_organization" text,
  "contact" text,
  "reachability" text
);

CREATE TABLE "volunteer" (
  "id" integer PRIMARY KEY,
  "name" text,
  "contact" text,
  "address" text,
  "oid" integer
);

CREATE TABLE "shelter" (
  "id" integer PRIMARY KEY,
  "lid" integer,
  "name" text,
  "contact" text,
  "address" text,
  "max_capacity" integer,
  "current_capacity" integer
);

CREATE TABLE "emergency_Service" (
  "id" integer PRIMARY KEY,
  "lid" integer,
  "name" text,
  "contact" text,
  "num_of_personnel" integer,
  "speed_of_response" text
);

CREATE TABLE "incident" (
  "id" integer PRIMARY KEY,
  "did" integer,
  "lid" integer,
  "date_time" timestamp,
  "description" text,
  "severity" text,
  "status" text,
  "active" integer,
  "monitoring_bureau" text,
  "reqd_funds" integer,
  "affected_population" integer,
  "reqd_volunteers" integer
);

CREATE TABLE "incident_funding" (
  "iid" integer,
  "fid" integer
);

CREATE TABLE "incident_resource_allocation" (
  "iid" integer,
  "eid" integer
);

CREATE TABLE "incident_volunteer_allotment" (
  "iid" integer,
  "vid" integer
);

ALTER TABLE "volunteer" ADD FOREIGN KEY ("oid") REFERENCES "organization" ("id");

ALTER TABLE "shelter" ADD FOREIGN KEY ("lid") REFERENCES "locality" ("id");

ALTER TABLE "emergency_service" ADD FOREIGN KEY ("lid") REFERENCES "locality" ("id");

ALTER TABLE "incident" ADD FOREIGN KEY ("did") REFERENCES "disaster" ("id");

ALTER TABLE "incident" ADD FOREIGN KEY ("lid") REFERENCES "locality" ("id");

ALTER TABLE "incident_funding" ADD FOREIGN KEY ("iid") REFERENCES "incident" ("id");

ALTER TABLE "incident_funding" ADD FOREIGN KEY ("fid") REFERENCES "funding_source" ("id");

ALTER TABLE "incident_resource_allocation" ADD FOREIGN KEY ("iid") REFERENCES "incident" ("id");

ALTER TABLE "incident_resource_allocation" ADD FOREIGN KEY ("eid") REFERENCES "essential" ("id");

ALTER TABLE "incident_resource_allocation" ADD FOREIGN KEY ("iid") REFERENCES "incident" ("id");

ALTER TABLE "incident_resource_allocation" ADD FOREIGN KEY ("vid") REFERENCES "volunteer" ("id");
