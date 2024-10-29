DROP TABLE IF EXISTS Disaster, Locality, Funding_Source, Essential, Organization, Volunteer,
Shelter, Emergency_Service, Incident, Incident_Funding, Incident_Resource_Allocation, Incident_Volunteer_Allotment ;

CREATE TABLE "Disaster" (
  "id" integer PRIMARY KEY,
  "name" text,
  "description" text,
  "protocol" text
);

CREATE TABLE "Locality" (
  "id" integer PRIMARY KEY,
  "name" text,
  "geographical_size" text,
  "development_level" text
);

CREATE TABLE "Funding_Source" (
  "id" integer PRIMARY KEY,
  "name" text,
  "contract_terms" text,
  "renewal_period" integer,
  "std_amt_donated" integer,
  "contact" text,
  "type_of_organization" text
);

CREATE TABLE "Essential" (
  "id" integer PRIMARY KEY,
  "name" text,
  "price_per_unit" integer,
  "qty_in_stock" integer
);

CREATE TABLE "Organization" (
  "id" integer PRIMARY KEY,
  "name" text,
  "type_of_organization" text,
  "contact" text,
  "reachability" text
);

CREATE TABLE "Volunteer" (
  "id" integer PRIMARY KEY,
  "name" text,
  "contact" text,
  "address" text,
  "age" integer,
  "oid" integer
);

CREATE TABLE "Shelter" (
  "id" integer PRIMARY KEY,
  "lid" integer,
  "name" text,
  "contact" text,
  "address" text,
  "max_capacity" integer,
  "current_capacity" integer
);

CREATE TABLE "Emergency_Service" (
  "id" integer PRIMARY KEY,
  "lid" integer,
  "name" text,
  "contact" text,
  "num_of_personnel" integer,
  "speed_of_response" text
);

CREATE TABLE "Incident" (
  "id" integer PRIMARY KEY,
  "did" integer,
  "lid" integer,
  "severity" text,
  "status" text,
  "active" integer,
  "monitoring_bureau" text,
  "reqd_funds" integer,
  "affected_population" integer,
  "reqd_volunteers" integer
);

CREATE TABLE "Incident_Funding" (
  "iid" integer,
  "fid" integer
);

CREATE TABLE "Incident_Resource_Allocation" (
  "iid" integer,
  "eid" integer
);

CREATE TABLE "Incident_Volunteer_Allotment" (
  "iid" integer,
  "vid" integer
);

ALTER TABLE "Volunteer" ADD FOREIGN KEY ("oid") REFERENCES "Organization" ("id");

ALTER TABLE "Shelter" ADD FOREIGN KEY ("lid") REFERENCES "Locality" ("id");

ALTER TABLE "Emergency_Service" ADD FOREIGN KEY ("lid") REFERENCES "Locality" ("id");

ALTER TABLE "Incident" ADD FOREIGN KEY ("did") REFERENCES "Disaster" ("id");

ALTER TABLE "Incident" ADD FOREIGN KEY ("lid") REFERENCES "Locality" ("id");

ALTER TABLE "Incident_Funding" ADD FOREIGN KEY ("iid") REFERENCES "Incident" ("id");

ALTER TABLE "Incident_Funding" ADD FOREIGN KEY ("fid") REFERENCES "Funding_Source" ("id");

ALTER TABLE "Incident_Resource_Allocation" ADD FOREIGN KEY ("iid") REFERENCES "Incident" ("id");

ALTER TABLE "Incident_Resource_Allocation" ADD FOREIGN KEY ("eid") REFERENCES "Essential" ("id");

ALTER TABLE "Incident_Volunteer_Allotment" ADD FOREIGN KEY ("iid") REFERENCES "Incident" ("id");

ALTER TABLE "Incident_Volunteer_Allotment" ADD FOREIGN KEY ("vid") REFERENCES "Volunteer" ("id");