BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "edge_types" (
	"id"	TEXT NOT NULL UNIQUE,
	"identifier"	TEXT,
	"name"	TEXT,
	"description"	TEXT DEFAULT 'None',
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "edges" (
	"id"	TEXT NOT NULL UNIQUE,
	"identifier"	TEXT,
	"source_node_id"	TEXT,
	"edge_type_id"	TEXT,
	"target_node_id"	TEXT,
	"description"	TEXT DEFAULT 'None',
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "nodes" (
	"id"	TEXT NOT NULL UNIQUE,
	"identifier"	TEXT,
	"name"	TEXT,
	"description"	TEXT DEFAULT 'None',
	PRIMARY KEY("id")
);
INSERT INTO "edge_types" VALUES ('20f50fa7-467c-4bb6-bb92-0fdee608904f',NULL,'- Default Edge Type -','None');
INSERT INTO "edge_types" VALUES ('07bef1cf-0b7c-420e-a04e-d03c69cb8e82',NULL,'has_type','None');
INSERT INTO "edge_types" VALUES ('74265995-5955-47be-a222-85f6566b3a99',NULL,'has_location','Nones');
INSERT INTO "edge_types" VALUES ('de709ce3-232b-4258-aab5-2f5ca95f4417',NULL,'includes_activity','None');
INSERT INTO "edge_types" VALUES ('83aec1e4-e2c0-4f22-bdce-80de64574513',NULL,'includes','None');
INSERT INTO "edge_types" VALUES ('829367e0-374f-4f75-97cb-08cf87511b70','','has_activity','None');
INSERT INTO "edge_types" VALUES ('71e3c128-954c-4a6d-8bd0-46b1cf320986','','includes_asset','Use to include an Asset in a Breakdown');
INSERT INTO "edge_types" VALUES ('f0def402-7630-4f93-b0c6-4c63a88fd4f5','','includes_something','None');
INSERT INTO "edges" VALUES ('a6352d9b-0d43-46f0-afbc-5c229c2c0259',NULL,'287d2c94-bc86-49cc-9707-b9903a500319','de709ce3-232b-4258-aab5-2f5ca95f4417','310e9150-12eb-4017-aa37-155eeae8a3ce','None');
INSERT INTO "edges" VALUES ('fdc72ab8-4c4d-44f9-bbf2-0414b97aa408',NULL,'287d2c94-bc86-49cc-9707-b9903a500319','de709ce3-232b-4258-aab5-2f5ca95f4417','87f7cfe3-6b2d-43a6-9899-64c146cf5749','None');
INSERT INTO "edges" VALUES ('0c53d882-a9b3-40b5-a19b-86eb7596f522','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417','f8d8c353-f26a-4f5e-9a0a-f50f4b146876','None');
INSERT INTO "edges" VALUES ('686435bf-3fee-4ff1-9d15-9cdb3951397d','','287d2c94-bc86-49cc-9707-b9903a500319','de709ce3-232b-4258-aab5-2f5ca95f4417','df5c6740-d7e1-4d5c-8b91-fb5e3e5dcedc','None');
INSERT INTO "edges" VALUES ('54e83935-303b-483f-a0e3-fd8f6a52be09','','287d2c94-bc86-49cc-9707-b9903a500319','de709ce3-232b-4258-aab5-2f5ca95f4417','5df08cbf-0f91-42ad-81d1-8beb43fe4cd7','None');
INSERT INTO "edges" VALUES ('903b3b8e-cc2f-4770-8805-5a822c855552','','33e093d3-ec9c-4388-84e8-90a314187d77','de709ce3-232b-4258-aab5-2f5ca95f4417','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','None');
INSERT INTO "edges" VALUES ('03b03db0-7390-4311-831d-05fdb34b5172','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417','ef873721-0bd0-4bb7-8cd0-abedd572c98b','None');
INSERT INTO "edges" VALUES ('c1812d1b-b137-41f0-bb26-0aeb60d580df','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417','d8e64715-a658-47da-9636-c6dbfd272500','None');
INSERT INTO "edges" VALUES ('4313eee9-2020-4828-a7c2-100bdfe51814','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417','2286af63-70d2-4c53-9f04-6b9fbb2b5227','None');
INSERT INTO "edges" VALUES ('86424ebf-d125-45f8-ab4d-1d80466d1cc2','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417','8c306188-ec69-4ce5-9294-ef98b06cc2a2','None');
INSERT INTO "edges" VALUES ('7ab629fa-e61e-417f-a915-b7294526980e','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417','114bc55e-e5f5-495d-a625-621ccb62cd52','None');
INSERT INTO "edges" VALUES ('73fd728e-a623-487a-8389-8f62bc3c0493','','f2c7e327-49f5-4f9b-8329-bf55c98a934f','de709ce3-232b-4258-aab5-2f5ca95f4417','05a92cdc-5bd7-45e8-bb07-0378a1191fda','');
INSERT INTO "edges" VALUES ('5e59c2f6-c42c-4b04-a13b-e44a68add722','','f2c7e327-49f5-4f9b-8329-bf55c98a934f','de709ce3-232b-4258-aab5-2f5ca95f4417','6f92a9c9-833f-4c4b-b4a4-ef43dedce36e','');
INSERT INTO "edges" VALUES ('e0d87935-09ee-45ed-8c5a-62b19db50bc4','','00299f27-dac5-4a64-aeae-fc1fc598b92d','de709ce3-232b-4258-aab5-2f5ca95f4417','287d2c94-bc86-49cc-9707-b9903a500319','');
INSERT INTO "edges" VALUES ('34f07fcd-91e7-4736-b5a0-c5b45cd8a671','','00299f27-dac5-4a64-aeae-fc1fc598b92d','de709ce3-232b-4258-aab5-2f5ca95f4417','33e093d3-ec9c-4388-84e8-90a314187d77','');
INSERT INTO "edges" VALUES ('3554fb85-b2be-4c7e-b53a-0d54b7a74275','','00299f27-dac5-4a64-aeae-fc1fc598b92d','de709ce3-232b-4258-aab5-2f5ca95f4417','f2c7e327-49f5-4f9b-8329-bf55c98a934f','');
INSERT INTO "edges" VALUES ('46875cfd-9463-421f-afb8-871a7f0eeeb7','','00299f27-dac5-4a64-aeae-fc1fc598b92d','de709ce3-232b-4258-aab5-2f5ca95f4417','53a8a4a5-e001-4c79-a558-88a85d7aceba','');
INSERT INTO "nodes" VALUES ('dbdc6656-cb60-4137-a8b5-38744563c178','SRE','SRL East','None');
INSERT INTO "nodes" VALUES ('1b680f39-d614-4ab1-9113-f7331333b8e9','GWY','Glen Waverleys','None');
INSERT INTO "nodes" VALUES ('141b1ef6-5332-495a-b713-2ed7fc59533a','','Location','Location Attribute');
INSERT INTO "nodes" VALUES ('a8ee94c8-8655-4cf1-9a14-8fdf63413a7c','','- Default Node -','Placeholder Node');
INSERT INTO "nodes" VALUES ('04a92c9d-9e38-492f-b9f9-e56e5432e31c','Ac','Activity','Uniclass Classification');
INSERT INTO "nodes" VALUES ('287d2c94-bc86-49cc-9707-b9903a500319','Ac_20 ','Administrative, Commercial and Protective Services Activities','None');
INSERT INTO "nodes" VALUES ('87f7cfe3-6b2d-43a6-9899-64c146cf5749','Ac_20_50','Commercial Activities','None');
INSERT INTO "nodes" VALUES ('310e9150-12eb-4017-aa37-155eeae8a3ce','Ac_20_15','Administrative Office Activities','None');
INSERT INTO "nodes" VALUES ('df5c6740-d7e1-4d5c-8b91-fb5e3e5dcedc','Ac_20_85','Security Activities','None');
INSERT INTO "nodes" VALUES ('5df08cbf-0f91-42ad-81d1-8beb43fe4cd7','Ac_20_90','Incident Support Activities','None');
INSERT INTO "nodes" VALUES ('33e093d3-ec9c-4388-84e8-90a314187d77','Ac_80','Transport Activities','None');
INSERT INTO "nodes" VALUES ('dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','Ac_80_10','Loading and Embarkation Activities','None');
INSERT INTO "nodes" VALUES ('ef873721-0bd0-4bb7-8cd0-abedd572c98b','Ac_80_10_60','Passenger Arriving','None');
INSERT INTO "nodes" VALUES ('d8e64715-a658-47da-9636-c6dbfd272500','Ac_80_10_61','Passenger Departing','None');
INSERT INTO "nodes" VALUES ('53a8a4a5-e001-4c79-a558-88a85d7aceba','Ac_85','Operation and Maintenance Activities','None');
INSERT INTO "nodes" VALUES ('6f92a9c9-833f-4c4b-b4a4-ef43dedce36e','Ac_80_50_90','Train Stopping','None');
INSERT INTO "nodes" VALUES ('05a92cdc-5bd7-45e8-bb07-0378a1191fda','Ac_80_50_75','Railway Travel','None');
INSERT INTO "nodes" VALUES ('f2c7e327-49f5-4f9b-8329-bf55c98a934f','Ac_80_50','Railway Activities','None');
INSERT INTO "nodes" VALUES ('114bc55e-e5f5-495d-a625-621ccb62cd52','Ac_80_10_86','Ticketing','None');
INSERT INTO "nodes" VALUES ('8c306188-ec69-4ce5-9294-ef98b06cc2a2','Ac_80_10_64','Passenger Gathering','None');
INSERT INTO "nodes" VALUES ('f8d8c353-f26a-4f5e-9a0a-f50f4b146876','Ac_80_10_63','Passenger Embarking','None');
INSERT INTO "nodes" VALUES ('2286af63-70d2-4c53-9f04-6b9fbb2b5227','Ac_80_10_62','Passenger Disembarking','None');
INSERT INTO "nodes" VALUES ('df89bad9-903a-4e50-8a24-947b3b11bb1a','BUR','Burwood Station','None');
INSERT INTO "nodes" VALUES ('966fad4f-ef61-4176-a726-4a3de04ab15e','SRL','Suburban Rail Loop','None');
INSERT INTO "nodes" VALUES ('0a039020-02a2-41cd-86bb-d728d1368ef7','SRN','SRL North','None');
INSERT INTO "nodes" VALUES ('00299f27-dac5-4a64-aeae-fc1fc598b92d','ABS','Activity Breakdown Structure','');
INSERT INTO "nodes" VALUES ('38a33ab9-c3b4-4f72-82b5-f172b2757062','L-2','[Name the Loss]','STPA Analysis');
COMMIT;
