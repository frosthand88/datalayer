CREATE TABLE researcher (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE paper (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL
);

CREATE TABLE topic (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE conference (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  year INT
);

CREATE TABLE organization (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE researcher_paper (
  researcher_id INT REFERENCES researcher(id),
  paper_id INT REFERENCES paper(id),
  PRIMARY KEY (researcher_id, paper_id)
);

CREATE TABLE paper_topic (
  paper_id INT REFERENCES paper(id),
  topic_id INT REFERENCES topic(id),
  PRIMARY KEY (paper_id, topic_id)
);

CREATE TABLE topic_conference (
  topic_id INT REFERENCES topic(id),
  conference_id INT REFERENCES conference(id),
  PRIMARY KEY (topic_id, conference_id)
);

CREATE TABLE conference_org (
  conference_id INT REFERENCES conference(id),
  org_id INT REFERENCES organization(id),
  PRIMARY KEY (conference_id, org_id)
);

-- Add some boolean, date, JSONB, and large text fields
--ALTER TABLE researcher ADD COLUMN is_active BOOLEAN DEFAULT true;
--ALTER TABLE researcher ADD COLUMN bio TEXT;  -- large text field
--ALTER TABLE paper ADD COLUMN published_at DATE;
--ALTER TABLE paper ADD COLUMN abstract TEXT;  -- large text field
--ALTER TABLE topic ADD COLUMN metadata JSONB;  -- flexible data (JSON)
--ALTER TABLE conference ADD COLUMN start_date DATE;
--ALTER TABLE organization ADD COLUMN website_url TEXT;

-- Simulate nullable relationships (some papers might not have a conference)
--ALTER TABLE paper ADD COLUMN conference_id INT REFERENCES conference(id);

