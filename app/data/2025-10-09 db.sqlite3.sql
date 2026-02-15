BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "breakdowns" (
	"id"	TEXT NOT NULL UNIQUE,
	"breakdown_node_id"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
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
	"weight"	INTEGER DEFAULT 1,
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
INSERT INTO "edge_types" VALUES ('74265995-5955-47be-a222-85f6566b3a99',NULL,'has_location','None');
INSERT INTO "edge_types" VALUES ('de709ce3-232b-4258-aab5-2f5ca95f4417',NULL,'includes_activity','None');
INSERT INTO "edge_types" VALUES ('83aec1e4-e2c0-4f22-bdce-80de64574513',NULL,'includes_location','None');
INSERT INTO "edge_types" VALUES ('829367e0-374f-4f75-97cb-08cf87511b70',NULL,'has_activity','None');
INSERT INTO "edge_types" VALUES ('71e3c128-954c-4a6d-8bd0-46b1cf320986',NULL,'includes_asset','Use to create an Asset Breakdown Structure (ABS)');
INSERT INTO "edge_types" VALUES ('f0def402-7630-4f93-b0c6-4c63a88fd4f5',NULL,'includes_something','None');
INSERT INTO "edge_types" VALUES ('c2e2587a-91df-47e5-9cec-ce0451e24f72',NULL,'includes_stage','Used to create a Product Life Cycle per ISO 24748');
INSERT INTO "edge_types" VALUES ('f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',NULL,'includes_process','None');
INSERT INTO "edge_types" VALUES ('608326ec-f163-46c4-af4a-22421c1f60bd',NULL,'includes','Generic Relationship for use where there is no applicable Specific Relationship');
INSERT INTO "edges" VALUES ('a6352d9b-0d43-46f0-afbc-5c229c2c0259','','287d2c94-bc86-49cc-9707-b9903a500319','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'310e9150-12eb-4017-aa37-155eeae8a3ce','None');
INSERT INTO "edges" VALUES ('fdc72ab8-4c4d-44f9-bbf2-0414b97aa408','','287d2c94-bc86-49cc-9707-b9903a500319','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'87f7cfe3-6b2d-43a6-9899-64c146cf5749','None');
INSERT INTO "edges" VALUES ('0c53d882-a9b3-40b5-a19b-86eb7596f522','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'f8d8c353-f26a-4f5e-9a0a-f50f4b146876','None');
INSERT INTO "edges" VALUES ('686435bf-3fee-4ff1-9d15-9cdb3951397d','','287d2c94-bc86-49cc-9707-b9903a500319','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'df5c6740-d7e1-4d5c-8b91-fb5e3e5dcedc','None');
INSERT INTO "edges" VALUES ('54e83935-303b-483f-a0e3-fd8f6a52be09','','287d2c94-bc86-49cc-9707-b9903a500319','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'5df08cbf-0f91-42ad-81d1-8beb43fe4cd7','None');
INSERT INTO "edges" VALUES ('903b3b8e-cc2f-4770-8805-5a822c855552','','33e093d3-ec9c-4388-84e8-90a314187d77','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','None');
INSERT INTO "edges" VALUES ('03b03db0-7390-4311-831d-05fdb34b5172','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'ef873721-0bd0-4bb7-8cd0-abedd572c98b','None');
INSERT INTO "edges" VALUES ('c1812d1b-b137-41f0-bb26-0aeb60d580df','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'d8e64715-a658-47da-9636-c6dbfd272500','None');
INSERT INTO "edges" VALUES ('4313eee9-2020-4828-a7c2-100bdfe51814','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'2286af63-70d2-4c53-9f04-6b9fbb2b5227','None');
INSERT INTO "edges" VALUES ('86424ebf-d125-45f8-ab4d-1d80466d1cc2','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'8c306188-ec69-4ce5-9294-ef98b06cc2a2','None');
INSERT INTO "edges" VALUES ('7ab629fa-e61e-417f-a915-b7294526980e','','dcaf99c2-26e8-4cd6-aa1d-7e8ada2968b2','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'114bc55e-e5f5-495d-a625-621ccb62cd52','None');
INSERT INTO "edges" VALUES ('73fd728e-a623-487a-8389-8f62bc3c0493','','f2c7e327-49f5-4f9b-8329-bf55c98a934f','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'05a92cdc-5bd7-45e8-bb07-0378a1191fda','None');
INSERT INTO "edges" VALUES ('5e59c2f6-c42c-4b04-a13b-e44a68add722','','f2c7e327-49f5-4f9b-8329-bf55c98a934f','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'6f92a9c9-833f-4c4b-b4a4-ef43dedce36e','None');
INSERT INTO "edges" VALUES ('e0d87935-09ee-45ed-8c5a-62b19db50bc4','','00299f27-dac5-4a64-aeae-fc1fc598b92d','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'287d2c94-bc86-49cc-9707-b9903a500319','None');
INSERT INTO "edges" VALUES ('34f07fcd-91e7-4736-b5a0-c5b45cd8a671','','00299f27-dac5-4a64-aeae-fc1fc598b92d','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'33e093d3-ec9c-4388-84e8-90a314187d77','None');
INSERT INTO "edges" VALUES ('3554fb85-b2be-4c7e-b53a-0d54b7a74275','','00299f27-dac5-4a64-aeae-fc1fc598b92d','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'f2c7e327-49f5-4f9b-8329-bf55c98a934f','None');
INSERT INTO "edges" VALUES ('46875cfd-9463-421f-afb8-871a7f0eeeb7','','00299f27-dac5-4a64-aeae-fc1fc598b92d','de709ce3-232b-4258-aab5-2f5ca95f4417',1,'53a8a4a5-e001-4c79-a558-88a85d7aceba','None');
INSERT INTO "edges" VALUES ('baacd8d6-4ae2-4245-b009-16dd218d6400','','966fad4f-ef61-4176-a726-4a3de04ab15e','83aec1e4-e2c0-4f22-bdce-80de64574513',1,'dbdc6656-cb60-4137-a8b5-38744563c178','None');
INSERT INTO "edges" VALUES ('c29bd0b5-e849-4a47-9d38-0f8b5d5f4c60','','966fad4f-ef61-4176-a726-4a3de04ab15e','83aec1e4-e2c0-4f22-bdce-80de64574513',1,'0a039020-02a2-41cd-86bb-d728d1368ef7','None');
INSERT INTO "edges" VALUES ('6a6de489-0fd3-4428-8334-84eaca1180b4','','966fad4f-ef61-4176-a726-4a3de04ab15e','83aec1e4-e2c0-4f22-bdce-80de64574513',1,'1efcba0c-8b97-49f0-a08e-0c79f6e096b9','None');
INSERT INTO "edges" VALUES ('3c015c5a-1dfd-442d-b48f-3eac28c44ec0','','966fad4f-ef61-4176-a726-4a3de04ab15e','83aec1e4-e2c0-4f22-bdce-80de64574513',1,'70672a40-2642-494b-99af-2d2f0bfc802d','None');
INSERT INTO "edges" VALUES ('ce425ae0-c046-4fc2-ac30-cad764f00d36','','e738ce00-a0f1-4b2a-9921-2ac538bd753f','c2e2587a-91df-47e5-9cec-ce0451e24f72',1,'d4abc91c-ce9b-4bb9-b315-d9f965995424','None');
INSERT INTO "edges" VALUES ('d735666c-15aa-41d1-97e7-07f9b36d5647','','e738ce00-a0f1-4b2a-9921-2ac538bd753f','c2e2587a-91df-47e5-9cec-ce0451e24f72',1,'1389d383-1af0-4ff8-8939-943cfbea062c','None');
INSERT INTO "edges" VALUES ('f41b76d4-2f7b-4a91-b2c9-62612250bf05','','e738ce00-a0f1-4b2a-9921-2ac538bd753f','c2e2587a-91df-47e5-9cec-ce0451e24f72',1,'ba08b2bb-9f40-4f47-9691-474730bd3927','None');
INSERT INTO "edges" VALUES ('1a07b961-901d-4d10-ac6b-111aface7438','','e738ce00-a0f1-4b2a-9921-2ac538bd753f','c2e2587a-91df-47e5-9cec-ce0451e24f72',1,'38ac9976-e9a8-40e5-b74d-f4431da05012','None');
INSERT INTO "edges" VALUES ('20c16c01-6072-47c7-b442-715d3056dd8e','','e738ce00-a0f1-4b2a-9921-2ac538bd753f','c2e2587a-91df-47e5-9cec-ce0451e24f72',1,'0d90993c-9962-4be4-8304-bec405412025','None');
INSERT INTO "edges" VALUES ('f00ac1bc-5a8b-409a-a969-5376e31530c7','','e738ce00-a0f1-4b2a-9921-2ac538bd753f','c2e2587a-91df-47e5-9cec-ce0451e24f72',1,'bac56765-e4e2-4a45-a6cc-027b9290ba43','None');
INSERT INTO "edges" VALUES ('5800bfae-8563-45d6-880b-410d61283009','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'08d86973-e83b-4cd1-998a-db0dbaa26845','None');
INSERT INTO "edges" VALUES ('2d01dc0d-169e-4c9a-a0b9-2ecaf6f804a2','','dbdc6656-cb60-4137-a8b5-38744563c178','83aec1e4-e2c0-4f22-bdce-80de64574513',1,'acbbc93c-80e6-4dd6-9b10-3c4411d793a7','None');
INSERT INTO "edges" VALUES ('78d79d10-182b-4f93-9591-029db9c8a908','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'fab303cc-21c2-4ec0-8e4b-e5ab8944ad36','');
INSERT INTO "edges" VALUES ('a0093194-9bd0-424f-8af2-8cb4849a864b','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'b27ab008-a08f-462a-86e0-23f872b89e53','');
INSERT INTO "edges" VALUES ('30f769b2-9560-455d-8126-bf0f4d8061c9','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'5ebd75ad-c4b2-4450-8659-60564a83c9f0','None');
INSERT INTO "edges" VALUES ('08543b68-710a-456e-8f09-6c96c548e5ef','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'8c98f192-9b87-4748-b4da-673eeda16cea','None');
INSERT INTO "edges" VALUES ('505b1442-8763-4bab-aaca-d675b001a8ce','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'9e7bf5fc-936f-414b-98cc-fab305d73dc1','');
INSERT INTO "edges" VALUES ('70e771d9-1f89-4343-8d5e-872db9101c66','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'619843a3-f83a-492f-beb2-696194c9d6f2','');
INSERT INTO "edges" VALUES ('cedf74c7-9486-4f07-a82b-2e8aaf66b88d','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'dee22a02-2712-4eca-8286-f8279c9c0d6b','');
INSERT INTO "edges" VALUES ('2873eb64-6a4e-4736-b7cb-a77f36740d6c','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'afd4ac49-8be2-4adc-8fcd-50282be76c67','');
INSERT INTO "edges" VALUES ('862ad038-9097-43dd-a65b-2497a49a1604','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'bb057abf-6df2-40ff-87c1-45d13db920bc','');
INSERT INTO "edges" VALUES ('54eff961-3d0c-47cd-9378-5e0a46979315','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'228cc222-189f-4b41-89b2-cbbc6cc027b6','');
INSERT INTO "edges" VALUES ('4e331690-1b8c-41ea-a350-c84faa9735f8','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'7ad3c941-49bf-4494-92d0-5089eeb20242','None');
INSERT INTO "edges" VALUES ('bfdf56ab-207f-4382-a1e6-4ae9f990a795','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'1d712b39-728f-47f2-95f9-02004187ef2d','None');
INSERT INTO "edges" VALUES ('80ae2054-b527-43ed-975f-a16990f6239c','','07a448b9-712c-4349-bccd-f6d374cde761','f23e67b2-f8c7-40bc-b1f9-00410ec5ea7c',1,'7f87f2d4-c104-40ff-88ea-e1b6f3ab6f3c','None');
INSERT INTO "edges" VALUES ('29758ac0-5b7d-4e5a-92ce-dc2114426345','','6818b2b6-1668-42d5-8add-b627f4fb61f7','608326ec-f163-46c4-af4a-22421c1f60bd',1,'a8ee94c8-8655-4cf1-9a14-8fdf63413a7c','None');
INSERT INTO "edges" VALUES ('7ee7fd0f-93bf-4fc0-9c35-c97ad660074e','','d2f3359f-b4e7-4f60-bbd2-efd91cc4a67d','608326ec-f163-46c4-af4a-22421c1f60bd',1,'a8ee94c8-8655-4cf1-9a14-8fdf63413a7c','None');
INSERT INTO "edges" VALUES ('8a224d66-267e-40c7-985e-52dba907e48b','','dcc0fe58-bfcd-4623-9565-a1b8056ec8c5','608326ec-f163-46c4-af4a-22421c1f60bd',1,'a8ee94c8-8655-4cf1-9a14-8fdf63413a7c','None');
INSERT INTO "nodes" VALUES ('dbdc6656-cb60-4137-a8b5-38744563c178','SRE','SRL East','Cheltenham to Box HIll');
INSERT INTO "nodes" VALUES ('1b680f39-d614-4ab1-9113-f7331333b8e9','GWY','Glen Waverley','None');
INSERT INTO "nodes" VALUES ('141b1ef6-5332-495a-b713-2ed7fc59533a','','Location','Location Attribute');
INSERT INTO "nodes" VALUES ('a8ee94c8-8655-4cf1-9a14-8fdf63413a7c','','- Default Node -','Placeholder Node');
INSERT INTO "nodes" VALUES ('04a92c9d-9e38-492f-b9f9-e56e5432e31c','Ac','Activities','Uniclass Classification; used for the Functional Architecture');
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
INSERT INTO "nodes" VALUES ('0a039020-02a2-41cd-86bb-d728d1368ef7','SRN','SRL North','Box Hill to Melbourne Airport');
INSERT INTO "nodes" VALUES ('00299f27-dac5-4a64-aeae-fc1fc598b92d','ABS','Activity Breakdown Structure','None');
INSERT INTO "nodes" VALUES ('38a33ab9-c3b4-4f72-82b5-f172b2757062','L-2','[Name the Loss]','STPA Analysis');
INSERT INTO "nodes" VALUES ('acbbc93c-80e6-4dd6-9b10-3c4411d793a7','SSY','Southern Stabling Yard','None');
INSERT INTO "nodes" VALUES ('1efcba0c-8b97-49f0-a08e-0c79f6e096b9','SRW','SRL West','Sunshine to Werribee');
INSERT INTO "nodes" VALUES ('70672a40-2642-494b-99af-2d2f0bfc802d','SRA','SRL Airport','Melbourne Airport to Sunshine');
INSERT INTO "nodes" VALUES ('e738ce00-a0f1-4b2a-9921-2ac538bd753f','','Product Lifecycle','ISO 24748-1:2018 Systems and Software Engineering - Lifecycle Management - Part 1 - Guidelines for Life Cycle Management');
INSERT INTO "nodes" VALUES ('d4abc91c-ce9b-4bb9-b315-d9f965995424','','Concept Stage','None');
INSERT INTO "nodes" VALUES ('1389d383-1af0-4ff8-8939-943cfbea062c','','Development Stage','None');
INSERT INTO "nodes" VALUES ('ba08b2bb-9f40-4f47-9691-474730bd3927','','Production Stage','None');
INSERT INTO "nodes" VALUES ('38ac9976-e9a8-40e5-b74d-f4431da05012','','Utilisation Stage','None');
INSERT INTO "nodes" VALUES ('0d90993c-9962-4be4-8304-bec405412025','','Support Stage','None');
INSERT INTO "nodes" VALUES ('bac56765-e4e2-4a45-a6cc-027b9290ba43','','Retirement Stage','None');
INSERT INTO "nodes" VALUES ('07a448b9-712c-4349-bccd-f6d374cde761','6.4','Technical Processes','None');
INSERT INTO "nodes" VALUES ('08d86973-e83b-4cd1-998a-db0dbaa26845','6.4.1','Business or Mission Analysis Process','None');
INSERT INTO "nodes" VALUES ('64e3526d-5105-447b-aa11-ead849f59d65','ABS','Asset Breakdown Structure','None');
INSERT INTO "nodes" VALUES ('9c38192c-cf8d-43b3-8d46-f9d9581100f2','LBS','Location Breakdown Structure','None');
INSERT INTO "nodes" VALUES ('b27ab008-a08f-462a-86e0-23f872b89e53','6.4.2','Stakeholder Needs and Requirements Definition Process','None');
INSERT INTO "nodes" VALUES ('5ebd75ad-c4b2-4450-8659-60564a83c9f0','6.4.3','System Requirements Definition Process','None');
INSERT INTO "nodes" VALUES ('fab303cc-21c2-4ec0-8e4b-e5ab8944ad36','6.4.14','Disposal Process','None');
INSERT INTO "nodes" VALUES ('7f87f2d4-c104-40ff-88ea-e1b6f3ab6f3c','6.4.13','Maintenance Process','None');
INSERT INTO "nodes" VALUES ('8c98f192-9b87-4748-b4da-673eeda16cea','6.4.4','System Architecture Definition Process','None');
INSERT INTO "nodes" VALUES ('9e7bf5fc-936f-414b-98cc-fab305d73dc1','6.4.5','Design Definition Process','None');
INSERT INTO "nodes" VALUES ('619843a3-f83a-492f-beb2-696194c9d6f2','6.4.6','System Analysis Process','None');
INSERT INTO "nodes" VALUES ('dee22a02-2712-4eca-8286-f8279c9c0d6b','6.4.7','Implementation Process','None');
INSERT INTO "nodes" VALUES ('afd4ac49-8be2-4adc-8fcd-50282be76c67','6.4.8','Integration Process','None');
INSERT INTO "nodes" VALUES ('bb057abf-6df2-40ff-87c1-45d13db920bc','6.4.9','Verification Process','None');
INSERT INTO "nodes" VALUES ('228cc222-189f-4b41-89b2-cbbc6cc027b6','6.4.10','Transition Process','None');
INSERT INTO "nodes" VALUES ('7ad3c941-49bf-4494-92d0-5089eeb20242','6.4.11','Validation Process','None');
INSERT INTO "nodes" VALUES ('1d712b39-728f-47f2-95f9-02004187ef2d','6.4.12','Operation Process','None');
INSERT INTO "nodes" VALUES ('6818b2b6-1668-42d5-8add-b627f4fb61f7','PAC','Package Assurance Case','None');
INSERT INTO "nodes" VALUES ('d2f3359f-b4e7-4f60-bbd2-efd91cc4a67d','PSC','Package Safety Case','None');
INSERT INTO "nodes" VALUES ('dcc0fe58-bfcd-4623-9565-a1b8056ec8c5','PLS','Package LIfecycle Stage(s)','None');
COMMIT;
