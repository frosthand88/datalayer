CREATE TABLE researcher (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  name TEXT NOT NULL
);

CREATE TABLE paper (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  title TEXT NOT NULL
);

CREATE TABLE topic (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  name TEXT NOT NULL
);

CREATE TABLE conference (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
  name TEXT NOT NULL,
  year INT
);

CREATE TABLE organization (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT now(),
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
