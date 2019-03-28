--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6 (Ubuntu 10.6-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.6 (Ubuntu 10.6-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_sender_id_fkey;
ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_receiver_id_fkey;
ALTER TABLE ONLY public.compatibilities DROP CONSTRAINT compatibilities_user_id_fkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_name_key;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_pkey;
ALTER TABLE ONLY public.compatibilities DROP CONSTRAINT compatibilities_pkey;
ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
ALTER TABLE public.messages ALTER COLUMN msg_id DROP DEFAULT;
DROP SEQUENCE public.users_user_id_seq;
DROP TABLE public.users;
DROP SEQUENCE public.messages_msg_id_seq;
DROP TABLE public.messages;
DROP TABLE public.compatibilities;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: compatibilities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.compatibilities (
    user_id integer NOT NULL,
    activity_quest integer,
    talking_quest integer,
    weather_quest integer,
    distance_quest integer,
    track_quest integer,
    dogs_quest integer,
    kids_quest integer,
    music_quest integer,
    current_race_quest integer,
    why_quest integer
);


--
-- Name: messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.messages (
    msg_id integer NOT NULL,
    sender_id integer,
    receiver_id integer,
    message character varying(1000) NOT NULL,
    time_created timestamp with time zone DEFAULT now(),
    time_updated timestamp with time zone,
    original_msg_id boolean
);


--
-- Name: messages_msg_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.messages_msg_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: messages_msg_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.messages_msg_id_seq OWNED BY public.messages.msg_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    name character varying(200) NOT NULL,
    email character varying(250) NOT NULL,
    password character varying(50) NOT NULL,
    lat double precision NOT NULL,
    lng double precision NOT NULL,
    pace character varying,
    run_type character varying(50)
);


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: messages msg_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages ALTER COLUMN msg_id SET DEFAULT nextval('public.messages_msg_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: compatibilities; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.compatibilities (user_id, activity_quest, talking_quest, weather_quest, distance_quest, track_quest, dogs_quest, kids_quest, music_quest, current_race_quest, why_quest) FROM stdin;
1	1	2	2	2	1	2	1	3	2	3
2	2	3	2	1	2	1	2	3	3	2
3	3	3	2	2	2	3	3	3	3	3
4	3	1	2	3	1	3	2	2	1	2
5	1	3	3	2	2	2	3	2	1	1
6	2	1	3	1	2	2	2	3	2	3
7	3	3	3	2	3	3	1	1	2	1
8	2	3	3	1	3	2	3	2	1	2
9	3	2	2	2	2	1	1	2	2	2
10	1	1	2	3	1	3	3	3	1	3
11	3	1	2	3	3	2	2	2	2	3
12	2	1	3	2	1	3	3	2	2	2
13	1	1	1	2	1	2	1	2	1	2
14	2	2	3	1	3	3	3	1	1	2
15	1	3	3	3	3	2	1	3	1	3
16	1	3	1	3	2	2	1	3	3	2
17	1	1	2	3	2	3	2	3	2	2
18	2	3	1	2	1	2	3	2	2	3
19	2	1	2	1	3	1	3	3	1	3
20	1	1	1	1	2	3	1	3	1	3
21	1	1	1	2	3	2	1	3	1	2
22	2	2	2	3	2	2	3	1	1	3
23	1	1	1	1	3	2	3	1	3	3
24	3	3	3	3	3	1	2	2	1	1
25	3	1	3	1	1	2	2	3	3	2
26	3	2	1	2	2	1	2	2	3	2
27	1	3	1	2	3	2	1	2	3	1
28	1	2	3	1	3	3	3	3	3	1
29	2	2	1	1	3	1	2	1	2	3
30	2	1	1	3	1	2	2	3	2	3
31	3	2	2	3	3	3	3	2	3	3
32	3	1	1	2	1	2	1	1	2	1
33	2	3	3	2	1	1	3	2	1	3
34	3	1	2	3	3	3	1	3	1	2
35	2	1	2	3	2	1	2	2	1	2
36	3	3	2	2	3	3	3	2	3	2
37	2	3	2	1	1	3	1	2	1	3
38	3	3	1	2	3	1	2	3	3	1
39	2	2	1	1	2	2	1	1	3	1
40	2	3	3	3	1	3	1	2	3	3
41	1	3	1	2	3	2	2	2	2	1
42	2	1	2	2	2	3	3	3	1	3
43	3	1	3	1	2	2	3	2	2	2
44	1	1	1	2	3	1	1	2	1	1
45	1	2	3	3	2	2	1	2	2	1
46	2	1	3	2	1	3	2	3	2	2
47	1	1	1	1	1	3	2	2	1	3
48	3	3	2	3	2	3	2	1	2	3
49	2	3	2	2	3	2	2	2	2	1
50	2	2	2	3	2	3	3	3	3	1
51	1	3	3	2	2	1	1	2	3	3
52	1	3	3	2	1	2	2	2	3	3
53	1	3	1	1	2	2	2	3	3	2
54	3	3	2	1	1	3	1	2	1	1
55	1	2	3	3	3	3	1	3	3	2
56	3	3	3	3	3	2	2	2	1	2
57	3	3	2	3	1	1	1	3	3	2
58	2	3	3	3	3	2	2	1	2	3
59	3	2	2	3	3	1	2	1	1	1
60	1	1	3	2	2	2	2	1	1	2
61	2	2	3	2	3	3	2	2	3	1
62	3	1	3	1	1	1	2	3	2	3
63	3	3	2	2	2	2	1	1	2	1
64	2	3	2	1	3	3	2	3	3	2
65	1	1	2	1	1	3	2	1	1	1
66	1	3	1	2	2	1	2	2	1	2
67	1	3	3	2	1	2	2	3	1	1
68	1	3	1	1	1	3	3	3	1	3
69	2	2	2	3	2	1	1	1	3	2
70	2	1	1	3	3	2	1	1	3	1
71	1	3	3	3	2	3	2	2	3	1
72	1	1	3	1	2	2	2	1	3	1
73	2	2	1	2	2	2	1	2	3	1
74	1	2	3	2	3	1	2	1	1	2
75	1	2	3	1	1	1	1	3	3	1
76	1	1	3	2	1	2	2	1	2	2
77	2	1	3	1	2	3	1	3	2	3
78	3	2	2	2	3	3	3	3	3	3
79	1	3	3	2	2	1	2	2	3	2
80	2	1	1	3	1	3	3	2	2	1
81	1	2	1	1	3	3	3	3	1	3
82	2	2	2	1	2	3	1	3	2	1
83	2	3	1	3	1	3	3	3	3	1
84	3	2	2	3	2	1	3	2	2	3
85	1	2	3	2	3	1	2	1	2	1
86	3	3	3	2	1	1	2	1	1	3
87	1	3	2	1	1	3	3	3	3	2
88	2	1	1	3	2	1	1	3	3	2
89	1	3	3	2	3	1	1	3	2	3
90	1	2	3	1	3	2	2	2	3	2
91	1	3	1	1	3	3	2	2	1	2
92	3	3	3	3	1	2	3	2	3	3
93	1	2	1	3	2	3	2	2	2	3
94	2	2	2	1	2	1	3	1	2	3
95	3	1	2	1	3	2	1	1	3	3
96	1	3	2	1	3	2	1	3	3	1
97	1	2	3	1	3	3	2	1	1	3
98	3	1	2	3	3	1	1	1	2	2
99	2	3	3	1	2	1	3	2	2	1
100	2	1	3	3	1	2	2	1	2	3
101	3	2	2	2	1	1	2	2	1	1
102	3	3	2	2	3	2	1	3	2	3
103	3	1	3	2	1	1	2	2	1	2
104	1	3	2	3	3	2	1	3	2	1
105	2	3	1	3	2	3	1	2	2	3
106	1	3	3	2	1	2	2	3	1	2
107	2	1	3	2	3	3	2	1	2	1
108	2	1	2	1	2	3	3	1	2	1
109	1	3	3	3	3	2	1	3	2	2
110	2	2	3	1	1	1	1	3	2	1
111	2	2	2	1	1	1	3	1	3	3
112	3	3	1	3	1	2	2	3	2	2
113	3	1	1	2	1	2	1	1	2	1
114	2	1	3	2	1	3	1	1	2	2
115	3	1	3	3	3	1	1	1	2	1
116	1	2	2	2	3	3	1	3	3	1
117	2	1	2	1	2	1	2	3	3	2
118	1	3	1	2	3	1	2	1	1	1
119	2	1	2	1	3	1	3	1	2	3
120	1	3	3	1	1	2	1	2	2	2
121	2	2	3	1	2	3	2	2	3	3
122	1	1	3	1	1	3	3	1	3	2
123	3	3	2	3	2	1	1	2	1	1
124	3	2	3	2	2	3	2	2	3	2
125	1	1	2	2	1	1	1	3	3	1
126	1	1	3	2	2	3	3	2	1	1
127	2	3	1	2	1	1	2	1	2	2
128	1	3	2	3	1	1	2	2	3	2
129	3	3	1	3	2	1	2	3	2	2
130	2	1	1	2	2	2	3	3	1	1
131	3	2	1	2	3	1	3	3	3	1
132	1	1	1	1	2	2	2	1	2	3
133	2	3	3	3	2	3	3	3	1	3
134	2	3	1	3	1	3	3	2	1	1
135	3	2	1	1	1	1	3	2	3	1
136	3	3	1	2	1	1	1	3	1	3
137	2	1	2	2	3	2	1	2	2	3
138	3	1	3	2	2	3	2	1	2	2
139	2	3	2	1	1	2	3	3	2	2
140	1	1	2	1	1	1	1	1	3	2
141	3	1	2	3	3	2	1	2	3	1
142	3	1	2	1	1	2	3	3	2	2
143	1	1	2	1	2	3	1	3	1	1
144	1	3	2	3	3	2	3	1	2	2
145	1	3	2	1	2	3	1	3	3	1
146	2	3	3	2	3	1	2	3	1	3
147	2	1	3	1	1	1	3	1	3	2
148	2	2	3	1	3	3	1	2	1	2
149	3	1	1	2	2	1	2	2	2	2
150	1	1	3	1	1	1	2	3	3	3
151	1	2	1	1	3	1	2	2	3	2
152	2	3	2	2	2	2	3	1	1	3
153	3	2	1	1	3	3	1	2	3	2
154	1	3	3	3	3	3	3	3	3	3
155	1	3	1	2	1	2	2	2	2	3
156	1	3	2	1	1	2	2	2	1	3
157	1	2	1	3	2	3	3	2	2	2
158	1	2	3	3	1	3	3	2	2	3
159	2	2	3	2	2	2	2	2	3	2
160	2	2	1	2	1	3	2	1	1	2
161	1	1	2	2	2	3	3	3	1	2
162	2	2	2	1	2	1	2	1	2	2
163	3	1	2	3	1	1	3	2	1	1
164	2	2	2	3	2	2	2	2	2	1
165	1	2	2	3	3	1	3	1	2	1
166	3	3	2	3	2	3	1	1	2	1
167	3	3	2	2	2	3	1	2	3	3
168	1	2	1	3	1	1	1	1	1	2
169	1	2	3	1	1	2	1	2	3	3
170	1	2	2	3	1	3	1	3	3	2
171	2	1	2	2	1	1	2	1	2	1
172	2	1	2	2	1	3	2	2	3	3
173	3	2	2	2	1	1	1	2	1	1
174	1	2	1	3	2	3	2	2	3	2
175	1	3	1	3	1	1	1	2	1	2
176	2	2	2	3	1	2	1	1	1	2
177	2	3	3	3	2	3	3	2	3	1
178	1	3	3	2	2	1	1	2	1	3
179	3	1	2	2	3	3	2	1	2	3
180	1	3	1	3	1	1	3	1	3	2
181	1	2	2	3	1	1	1	1	2	3
182	1	1	2	1	1	1	3	3	2	1
183	2	3	3	1	1	1	1	3	1	3
184	2	3	1	2	2	3	3	1	2	3
185	1	3	3	3	3	1	2	3	1	1
186	3	3	2	3	2	3	3	2	3	3
187	1	3	2	1	1	1	1	1	1	1
188	3	2	3	3	3	3	1	1	2	2
189	3	1	1	3	2	3	2	3	3	2
190	3	3	2	3	1	3	1	1	2	3
191	1	3	2	3	2	1	2	3	3	3
192	1	1	3	1	2	3	3	1	3	3
193	3	2	2	1	2	3	3	1	3	1
194	1	3	2	1	1	3	3	3	1	3
196	3	3	3	3	2	2	2	2	3	2
197	1	1	1	1	1	1	1	1	1	1
198	1	1	1	1	1	1	1	1	1	1
199	3	3	3	3	3	3	3	3	3	3
200	1	3	3	3	3	3	3	3	3	3
201	2	3	3	3	3	3	3	3	3	3
205	1	2	3	2	3	2	1	2	2	2
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.messages (msg_id, sender_id, receiver_id, message, time_created, time_updated, original_msg_id) FROM stdin;
22	196	189	\n            Hi Michael!  I found your RunBuddy profile.  It seems like we might have a few things in common.  Are you free for a run this Friday?	2019-03-15 18:50:43.652129+00	\N	\N
23	196	201	\n            Hi, Josh!  Are you free for a run this Friday?  Let me know, thanks!	2019-03-15 18:59:48.774003+00	\N	\N
24	201	196	\n            Hi, Kirby!  Absolutely!  What time works best for you on Friday?  I prefer mornings, personally.  Does 7am work?	2019-03-15 19:01:32.050067+00	\N	\N
25	196	201	\n            Hi, Josh!  Yes, Friday morning works.  Should we meet at Washington Elementary?  	2019-03-15 19:04:01.131978+00	\N	\N
26	196	201	\n            Hi, Josh!  Are you free tomorrow for a quick 3 mile run?	2019-03-18 02:55:32.606505+00	\N	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (user_id, name, email, password, lat, lng, pace, run_type) FROM stdin;
1	Ashley Massey	obriencarla@murphy.com	h1mQ7_zl*1	37.5808284285714009	-122.347955591837007	12:00	trail
2	Tracey Davis	christopherewing@banks.com	o%wJ0Sp@2i	37.5797853500000016	-122.350649516203006	10:00	trail
3	James Warren	lopezwilliam@yahoo.com	S6g4)Zd+_4	37.5749018445916008	-122.342974709456001	7:30	both
4	Cynthia Harvey	heatherross@dickerson-moore.com	*3UNcXtsV_	37.5790178000000026	-122.348920827762996	9:00	trail
5	Abigail Cooper	zmitchell@yahoo.com	wV8r6OuMK+	37.5791709095137989	-122.346360073471004	9:15	trail
6	Martha Campbell	kimberly50@hill.com	V^d*0hHyyc	37.5892728380648009	-122.342895225955004	10:30	road
7	Casey Padilla	robin52@taylor.com	9WarKCy1&3	37.5780539264710995	-122.350269205065004	12:00	both
8	Alejandro Austin	pallen@gmail.com	Jw8*SYXa@!	37.5951079499999992	-122.366330675905004	9:45	both
9	Terri Brooks	amberwalker@yahoo.com	l6bMku0c#p	37.5793430351522986	-122.339989032698995	7:15	both
10	Jennifer West	christian52@yahoo.com	(0kOrFXP*g	37.5920119999999969	-122.358567996668995	8:30	road
11	Anthony Hunter	cindy47@gmail.com	27PqZpPH@B	37.5785707000000002	-122.3467184	9:15	trail
12	Robert Huff	seanmccoy@salas-stafford.biz	&Zn8PnBO3_	37.5859135306122027	-122.359809653061006	6:00	trail
13	Stacey Thomas	katherine68@shelton.org	&1XLmIyyAk	37.5860229999999973	-122.360068999999996	6:00	both
14	Tony Mendez	jamesfields@hanson-browning.net	V#Pf6mc(EK	37.5892728380648009	-122.342895225955004	10:00	trail
15	Angela Garrison	lozanojason@thompson.com	EA7hBjj$!2	37.5772756000000001	-122.348279572577994	9:15	road
16	Melissa Ramos	heidi22@lowery.info	_8SaooAYve	37.591083702886003	-122.347251628145003	7:45	road
17	Rachel Boyd	matthewchambers@hotmail.com	^$m2Amvjb*	37.5843196871173006	-122.348942747863006	7:15	road
18	Sandy Carson	markhawkins@patel.com	%0p28UkoiW	37.5822693313822995	-122.380556885245994	9:30	both
19	Dawn Hodges	khanwilliam@reed-henderson.org	V)$51KZh^R	37.5971503999999968	-122.372345899999999	10:00	trail
20	Steven Barrera	brianjacobs@yahoo.com	d#4KGXwwSK	37.5780987289539965	-122.348335283034999	8:15	trail
21	James Mcdonald	wdunn@hotmail.com	(OwxWHry$8	37.5742489952312013	-122.350015512444998	9:30	both
22	Ryan Adams	bjordan@day.com	R%8FRAg)qL	37.5742489952312013	-122.350015512444998	9:00	trail
23	Nicholas Alvarez	timothylandry@yahoo.com	C(G3TwvlqO	37.6030810000000031	-122.396291000000005	10:00	trail
24	Fernando Reilly	aguilarkenneth@moore.org	lVN4)WoB@n	37.5970570899051992	-122.396919641867996	8:15	road
25	Alexis Reeves	veronicawalters@gmail.com	uxN5JLgV+8	37.6002599642010011	-122.390177176609996	11:30	both
26	Kimberly Higgins	rodgersbrett@yahoo.com	6&c6d@z9DR	37.6001652902710006	-122.390732687581007	9:30	both
27	Stephanie Benson	sgoodwin@gmail.com	t4LcDi(D*H	37.5873924231798	-122.393823418422002	6:30	road
28	Nancy Fitzpatrick	johnscott@parker-hansen.com	m8O96ADq&z	37.602799217370297	-122.392699332679996	10:00	trail
29	Brad Hall	jberry@gmail.com	%useRaC9e8	37.6030810000000031	-122.396291000000005	6:30	both
30	Adam Hernandez	fstone@phillips-miranda.com	U@5IsQlE*6	37.6002599642010011	-122.390177176609996	7:30	both
31	Timothy Brennan	garciarichard@hotmail.com	*3GT3PHza5	37.6018626999999981	-122.3932073	6:45	both
32	Jon Johnston	uhudson@yahoo.com	%i)eiAq6+6	37.6023261570472016	-122.393710478201001	9:45	both
33	Haley Martin	qsmith@yahoo.com	@_aMGKVmM2	37.6025788000000034	-122.394197399999996	10:45	trail
34	Brian Hensley	mahoneyjohn@garcia.com	KdOf17Bh6&	37.6003187000000025	-122.383834399999998	11:30	both
35	Valerie Jones	lisabennett@yahoo.com	w9vHUiaz@f	37.5966248000000007	-122.381227956700997	6:30	road
36	Spencer Wright	michelle69@hotmail.com	E5GGfO(H%D	37.6002324261234975	-122.389537764452996	6:15	both
37	Jennifer Ortiz	brice@ortega-delacruz.com	!eY8il+vP8	37.5474789000000015	-122.315168168243005	7:45	both
38	Brandy Mccoy	maria51@yahoo.com	37WYptPH+v	37.5622710000000026	-122.317408999999998	10:30	trail
39	Luis Henderson	erinewing@odonnell.com	_krHZBhW24	37.5560665	-122.288257799999997	7:45	road
40	Sean Ali	iwilkerson@yahoo.com	HvCx4ZC$r&	37.5636968478109026	-122.285029188056001	11:45	road
41	Amy Osborne	belldanielle@martinez.info	!5BFghZa5p	37.5657775000000029	-122.324356699999996	7:00	trail
42	Sherry Benton	rpowell@carson.com	@9&Ceyqbw6	37.5534897000000001	-122.299521081877003	8:45	road
43	Tracy Morales	nicholasbates@silva.com	*jIrLlUh56	37.5608062158496026	-122.315469052346003	11:45	both
44	Sarah Patel	lthompson@cooper-smith.com	Qf7DDhP7g^	37.5493501396005982	-122.318558223511005	10:30	both
45	Anthony Parsons	josephlopez@gmail.com	$qKiPUTdW3	37.5431689999999989	-122.306602571428996	6:15	both
46	Michael Alexander	brianedwards@hotmail.com	8o%cR+xi!M	37.5574949897744972	-122.300937667986005	12:00	trail
47	Damon Garcia	reidjessica@hotmail.com	_9eBnopuor	37.5492193673469004	-122.308154428571001	7:45	both
48	Kerri Fernandez	larry30@hotmail.com	$3GmrU(UA@	37.5609248902509023	-122.328186425406003	10:15	road
49	Stephen Jackson	sarah78@ross-perez.com	EB18$5Hk+X	37.566631000000001	-122.3257002	10:45	both
50	Andrea Pierce	lopezpatrick@hobbs.biz	3h(22Gts(&	37.5741252565055035	-122.327856169639006	7:30	road
51	Aaron Payne	umcmahon@gmail.com	J&wLWum0(6	37.5708933593341996	-122.337051106960004	11:00	road
52	Patrick Miller	dbeck@wu.com	V9L397HbB!	37.5368825500000014	-122.324889299999995	9:00	road
53	Dustin Lang	rachel95@turner.com	*GFwvLPs44	37.5657775000000029	-122.324356699999996	6:30	road
54	Donna Vargas	taraburgess@gmail.com	pX2Rhjyk&9	37.5664620000000014	-122.324741000000003	12:00	both
55	Melissa Evans	martinezjames@yahoo.com	8qW8YFQn&Z	37.626754224489801	-122.411173040815996	7:45	trail
56	Kendra Johnson	sellersjeremiah@escobar-owen.com	U%0J_uGic_	37.6234119428571034	-122.411342185714005	9:15	trail
57	Mary Miranda	christine45@lopez-mendez.net	)niA+TDbs6	37.6257378000000031	-122.426077699999993	8:30	road
58	Ronald Aguilar	kristy28@sims.info	+6rgk2Gplo	37.6281269999999992	-122.422685000000001	11:00	both
59	Douglas Montes	cheryldavies@floyd.org	d^R1sXGaac	37.6281990332674994	-122.422062561645006	9:15	both
60	William Smith	melissa88@romero-robinson.org	qmp9zHw8$*	37.6210329999999971	-122.411118000000002	9:00	trail
61	Megan Smith	georgepatrick@gmail.com	)EXw1Idg6!	37.6285140000000027	-122.425752000000003	7:30	road
62	Diana Barker	grantchristopher@king.com	2K4OJvdp&d	37.6287828000000033	-122.422058121578999	6:30	both
63	Brandi Williams	wbrooks@morgan.com	p0S)D3Ooxv	37.6228669999999994	-122.412458799999996	9:15	trail
64	Amber Craig	robertnovak@gmail.com	)CWprij11E	37.6293809499999981	-122.418792748702003	10:45	road
65	Cindy Frazier	jgonzalez@miller.info	FD46GLtw+W	37.6400990210770985	-122.411656233518997	10:30	trail
66	Dr. Andrew Ochoa MD	danieljenkins@gmail.com	)1GLwxkw*Z	37.6279036470588011	-122.411404588235001	11:30	trail
67	Timothy Thomas	nicolas88@yahoo.com	#f9dRSYSl#	37.6348029143529033	-122.425517153729999	6:00	trail
68	Kevin Warren	adougherty@bray.org	M99YUenZ_S	37.6228669999999994	-122.412458799999996	9:15	trail
69	Melissa Williams	justinklein@hotmail.com	99sLW3r_#X	37.6257378000000031	-122.426077699999993	6:15	road
70	Lisa Hawkins	amberguerra@yahoo.com	fQ%SA8ro(4	37.6276444285714007	-122.416526775509993	9:00	trail
71	Cynthia Johnson	dwalker@hooper.com	b6AdxP$F#S	37.6519448545047979	-122.392817922150996	9:45	road
72	Stephen Long	joseph62@moore.info	#d1NI0VhuX	37.6539061052631965	-122.410664894736996	8:30	road
73	Evan Thompson	clarencekeller@yahoo.com	WYn*O9Sfm(	37.6454712706701002	-122.403631447663003	12:00	road
74	Stephanie Mata	sking@gmail.com	9(5RzxvtW(	37.6663761000000008	-122.398080800000002	12:00	road
75	Michael Riddle	thomaslyons@hotmail.com	$3aKErm#pd	37.6491741563619016	-122.385609287194001	9:45	road
76	Alyssa Long	erin54@ellis.net	@t00BOPU4s	37.672134100000001	-122.387714599999995	11:15	both
77	David Harding	smithlori@montgomery.biz	*g6yt@ne1C	37.6542138000000008	-122.389576562288994	10:45	road
78	Jessica Stanley	justin39@bell.com	C0O$9eJmRh	37.6557472713748993	-122.413106596969001	8:00	road
79	Jimmy Jensen	kim09@brown.com	rdI)hOdi*8	37.6533166561384007	-122.380707315883996	10:00	both
80	Ryan Martin	paulacampbell@montgomery.org	+s9N*CXZW8	37.6469203187763028	-122.399329354176999	8:45	trail
81	Mark Davis	garciacharlotte@yahoo.com	m&&6JIbe&J	37.654977256860299	-122.409617575357998	10:00	trail
82	Mrs. Julia Chandler MD	wandrews@sanchez.com	RD1OpOBu9+	37.6490101563619035	-122.385621287193999	11:00	road
83	Curtis Green Jr.	zfrye@smith.com	F)*N2I2b(c	37.6553016991150002	-122.406036088495995	7:30	road
84	Ashley Henderson	grahamjorge@schroeder.com	qL2E31Tr+_	37.6450491140188035	-122.416041214177	7:30	trail
85	Richard Davis	luis31@hotmail.com	!5(aGIyHbL	37.6522057113131012	-122.393316074507993	10:15	trail
86	Jack Reynolds	cynthia15@yahoo.com	5uWCrNVa$2	37.6522657429189991	-122.400225850702	7:00	trail
87	Brooke Holmes	gillespiejohn@hotmail.com	(U#3ZNnc_l	37.6729148000000009	-122.385924500000002	11:15	trail
88	Kevin Jenkins	staceylynch@yahoo.com	R^7RHq3+Jt	37.6645486000000034	-122.399010399999995	6:00	both
89	Justin Perez	kayla95@roberts-conway.info	PGyoz9dpL&	37.6401206999999971	-122.414607599999997	9:15	both
90	Melanie Torres	dunnolivia@mayo.com	0cbcY@(z%K	37.6520100687069004	-122.392942460239993	7:45	trail
91	Bryan Myers	brandonmurphy@gmail.com	#9TvSoen2#	37.6506808919823968	-122.387132829375005	10:15	both
92	Lorraine Henderson	angela08@bryant.com	T5Fy69LsV^	37.6413118080808005	-122.411514212121006	9:00	trail
93	Crystal Clarke	qmontes@yahoo.com	F5Lu089O_1	37.6428629999999984	-122.417769142856997	10:00	trail
94	David Brewer	ellisvictoria@travis-bruce.biz	37#WEsEz@7	37.6525570816327004	-122.411133877550995	9:00	both
95	Jeremy Hughes	rmedina@gmail.com	3ycQ)^FA^z	37.5808284285714009	-122.347955591837007	9:15	trail
96	Brianna Berry	chelsea48@mason.net	^FU2LTqOti	37.5797853500000016	-122.350649516203006	10:45	both
97	James Gonzalez	belloscar@hotmail.com	zR4Y2ay_G&	37.5749018445916008	-122.342974709456001	6:30	both
98	Stanley Williams	woodsjoshua@yahoo.com	^Cn$W!cgk6	37.5790178000000026	-122.348920827762996	7:15	trail
99	Glenn Lopez	morgan35@yahoo.com	G%JPy7Tpo$	37.5791709095137989	-122.346360073471004	6:00	trail
100	Kevin Taylor	bennettkelly@page.com	27&6JSdIT$	37.5892728380648009	-122.342895225955004	9:45	trail
101	Joshua Hartman	hughestammy@hotmail.com	)L&4vgUt)U	37.5780539264710995	-122.350269205065004	10:30	road
102	Stephen Webster	madison68@harris.com	s%3DSShs!@	37.5951079499999992	-122.366330675905004	8:45	both
103	Samuel Dorsey	ohowell@cooper.com	@l#7XGspY7	37.5793430351522986	-122.339989032698995	9:15	trail
104	Carlos Williams	rebeccaharris@tucker-clark.com	LvN0+Qsd))	37.5920119999999969	-122.358567996668995	7:00	trail
105	Nicholas Hampton	kwang@hebert-hart.com	c@1U4HstkH	37.5785707000000002	-122.3467184	11:30	both
106	Julia Turner	weavermichael@hayes.info	s9!)4XmE#f	37.5859135306122027	-122.359809653061006	10:15	both
107	John Glover	isnyder@yahoo.com	)8ZOVXa7eH	37.5860229999999973	-122.360068999999996	12:00	trail
108	Rachel Farmer	pnelson@gmail.com	5I&0SiZU@o	37.5892728380648009	-122.342895225955004	10:00	trail
109	Lisa Mathews	stacey15@foster.info	P(7JSMaY5!	37.5772756000000001	-122.348279572577994	6:15	both
110	Mr. George Bean	stephen61@gmail.com	$9XIgB!@oR	37.591083702886003	-122.347251628145003	8:15	trail
111	Heidi Robles	benjaminmeyers@hotmail.com	CF9Jd+65@C	37.5843196871173006	-122.348942747863006	6:15	both
112	Melissa Arnold	bradleycourtney@hamilton.com	@7LM11uRq*	37.5822693313822995	-122.380556885245994	10:00	trail
113	Rebecca Collins	amy86@murphy.org	ZSgREeWv@5	37.5971503999999968	-122.372345899999999	11:45	trail
114	Jennifer Sanders	vnelson@medina-riley.biz	_F2^NxnmT@	37.5780987289539965	-122.348335283034999	9:15	trail
115	Sandra Marshall	bbrewer@gmail.com	*Z6XFPOdAy	37.5742489952312013	-122.350015512444998	9:00	both
116	Gregory Morales	erikajimenez@gmail.com	)^aKyJgh4t	37.5742489952312013	-122.350015512444998	7:00	trail
117	Jeff Hunt	lesliewright@yahoo.com	E*3SvLlqsx	37.6030810000000031	-122.396291000000005	9:15	both
118	Justin Barnett	miguel16@hotmail.com	++i3%Cs+hQ	37.5970570899051992	-122.396919641867996	6:45	both
119	Jared Avila	john64@hotmail.com	hP3Aj7aXg&	37.6002599642010011	-122.390177176609996	8:30	both
120	Jeremy Gordon	colin27@walker-keith.net	6q4p)7Mr&N	37.6001652902710006	-122.390732687581007	9:45	road
121	Victoria Gilbert	hsilva@hotmail.com	6!7Rtqi%EL	37.5873924231798	-122.393823418422002	6:45	road
122	Todd Smith	bward@gmail.com	7ONDyZcI*@	37.602799217370297	-122.392699332679996	6:15	trail
123	Molly Smith	ashleysoto@adams-wallace.info	+@&6AvLsjF	37.6030810000000031	-122.396291000000005	10:45	road
124	Lori Lopez	josephpayne@gmail.com	y9a4wSKu!H	37.6002599642010011	-122.390177176609996	6:00	road
125	Vicki Ruiz	khernandez@hotmail.com	_1QdmNqbUA	37.6018626999999981	-122.3932073	7:00	both
126	Daniel Hawkins	charlesdavis@gmail.com	5TOItYUb+s	37.6023261570472016	-122.393710478201001	11:30	trail
127	Gordon Aguilar	wendywhite@gmail.com	_Q6DeHNrq8	37.6025788000000034	-122.394197399999996	6:45	road
128	Patricia Bradley	erin36@yahoo.com	@%#3OY!t4E	37.6003187000000025	-122.383834399999998	7:45	both
129	Ian Graves	smithleah@yahoo.com	9S#O2Ud!d$	37.5966248000000007	-122.381227956700997	10:15	both
130	Carol Hendricks	fburns@warren.net	5RCkf&xo(P	37.6002324261234975	-122.389537764452996	7:45	trail
131	George Hill	katelyn66@aguirre.net	_N8eNSlxkO	37.5474789000000015	-122.315168168243005	10:30	trail
132	Cameron Garcia	khawkins@gonzalez-mullins.com	wQ_4GJbvKO	37.5622710000000026	-122.317408999999998	9:45	road
133	Joseph Robinson	andrewwells@hotmail.com	#d5B#y7ios	37.5560665	-122.288257799999997	9:30	both
134	Raymond Tucker	wayne68@hotmail.com	k4SbEfyl(0	37.5636968478109026	-122.285029188056001	6:00	trail
135	Jeremy Hood	scastro@bates-oconnell.info	^zcNcSq!71	37.5657775000000029	-122.324356699999996	12:00	trail
136	Kayla Hall	bellpamela@carter.biz	!3eU9bl+rw	37.5534897000000001	-122.299521081877003	10:00	both
137	Dakota Hughes	marquezcesar@hotmail.com	vCJIW8Vy^W	37.5608062158496026	-122.315469052346003	11:00	both
138	Christopher Bell	jamesthomas@ponce.com	u+#3BAyGtp	37.5493501396005982	-122.318558223511005	10:00	trail
139	Jamie Carlson	kathybowman@todd.biz	$+7BTXmxJN	37.5431689999999989	-122.306602571428996	10:15	road
140	Sheryl Jones	matthewsjessica@hotmail.com	t1XNPXYg+m	37.5574949897744972	-122.300937667986005	7:00	road
141	Jason Bartlett	hingram@oliver-hill.com	(2s+FisILd	37.5492193673469004	-122.308154428571001	7:15	trail
142	Amanda Booker	cwebb@gmail.com	aSC9_1qu)1	37.5609248902509023	-122.328186425406003	7:00	road
143	Justin Zuniga	samuel69@gutierrez.net	6T%tG2o1&+	37.566631000000001	-122.3257002	9:30	both
144	Michael Gonzalez	hinesjonathan@gmail.com	*rmNmt9bY0	37.5741252565055035	-122.327856169639006	7:15	both
145	Steven Frazier	wacosta@frey.com	VSfY!JwY%1	37.5708933593341996	-122.337051106960004	9:00	both
146	Anita Santana	xbowen@hotmail.com	$VrVkrgMq5	37.5368825500000014	-122.324889299999995	9:45	both
147	Terri Frazier	lucasstewart@hotmail.com	!GPXFZhwd1	37.5657775000000029	-122.324356699999996	9:45	trail
148	Theresa Rhodes	kevinroberts@gmail.com	^+vs4FacIX	37.5664620000000014	-122.324741000000003	7:15	road
149	Jason Jimenez	davidwatkins@martin.com	^^3CcOjZZb	37.626754224489801	-122.411173040815996	6:00	both
150	Monique Rogers	scott23@robertson-davis.info	+2Z0VhRgg(	37.6234119428571034	-122.411342185714005	8:15	road
151	Brian Hayes	qcook@white.biz	O5pMl5Vg%B	37.6257378000000031	-122.426077699999993	10:30	both
152	Monica Robinson	jilljohnson@williams.org	$7CCg)#!aY	37.6281269999999992	-122.422685000000001	8:30	trail
153	Lisa Myers	tayloroneal@yahoo.com	YW#*3*Bv(H	37.6281990332674994	-122.422062561645006	7:45	road
154	Levi Wilson	lloydwilliam@gomez.com	#hROqzen)1	37.6210329999999971	-122.411118000000002	7:00	trail
155	Jill Taylor	novakdenise@mitchell-hammond.com	%90GK#wI)b	37.6285140000000027	-122.425752000000003	10:30	road
156	Melissa Murphy	wmills@lawrence.info	a)4V_rrZJT	37.6287828000000033	-122.422058121578999	9:00	trail
157	Nicole Harrison	urodriguez@banks-moore.net	Jw7J*bK1$b	37.6228669999999994	-122.412458799999996	10:30	trail
158	Darryl Ashley	yorkjerry@buck-gonzalez.com	%jS0ZN^ny+	37.6293809499999981	-122.418792748702003	6:45	road
159	Michael Wolfe	christineharris@jones.com	+Agk66KSb9	37.6400990210770985	-122.411656233518997	7:30	both
160	Darlene Scott	tiffany64@smith-gaines.com	!u8MbD)sY(	37.6279036470588011	-122.411404588235001	9:15	trail
161	Earl Jones	kathleen52@yahoo.com	!JZDP9nFo0	37.6348029143529033	-122.425517153729999	12:00	both
162	Christina Webb	igamble@yahoo.com	G3A_gvBw*7	37.6228669999999994	-122.412458799999996	7:15	both
163	Michelle Odonnell	mcgeelindsay@white.com	p75E_JMf*5	37.6257378000000031	-122.426077699999993	11:30	trail
164	James Williams	christopher38@white-morales.biz	Ct3CQGa!%6	37.6276444285714007	-122.416526775509993	11:15	road
165	Mary Johnson	bryce34@miranda.com	JU)Y9Lyud(	37.6519448545047979	-122.392817922150996	11:00	trail
166	Derrick Moore	sullivanchristina@harvey.com	*OH0mTdF*7	37.6539061052631965	-122.410664894736996	8:30	trail
167	Dr. Savannah Everett	lbarker@conway.com	E7Qc2Qws#(	37.6454712706701002	-122.403631447663003	9:30	road
168	Nathan Bennett	katie12@carpenter.biz	+S46ZkYIF3	37.6663761000000008	-122.398080800000002	6:45	road
169	Jacob Lewis	gbarnes@yahoo.com	MH7l(LfhA!	37.6491741563619016	-122.385609287194001	6:45	both
170	Gail Burton	younggeorge@campbell.org	$PCYu2Rxu2	37.672134100000001	-122.387714599999995	11:00	road
171	Susan Pena	wwelch@hotmail.com	%@YEJja2&9	37.6542138000000008	-122.389576562288994	9:15	trail
172	Richard Fox	rodriguezmarc@hotmail.com	flZAWYz((0	37.6557472713748993	-122.413106596969001	11:15	trail
173	Caleb Martinez	llong@mitchell.com	2fRwihId+4	37.6533166561384007	-122.380707315883996	9:30	both
174	Deborah Long	joseph44@gmail.com	$0wU9UQ0jM	37.6469203187763028	-122.399329354176999	10:15	trail
175	Kyle Robinson	madams@yahoo.com	M)@)1TwrJh	37.654977256860299	-122.409617575357998	8:00	both
176	Elizabeth Scott	carmenking@obrien.com	6DGRLEwR&j	37.6490101563619035	-122.385621287193999	7:00	trail
177	Janice Fields	emills@yahoo.com	V6RSqjy(&4	37.6553016991150002	-122.406036088495995	9:45	trail
178	Marissa Simmons	michellejones@frederick.com	LD@1QYOmeG	37.6450491140188035	-122.416041214177	12:00	both
179	Michael Kline	flemingheather@jones-king.com	@q$32UYtM5	37.6522057113131012	-122.393316074507993	6:30	both
180	Ann Rodriguez	williamfarmer@gmail.com	%j32WK)o$%	37.6522657429189991	-122.400225850702	11:00	both
181	Jamie Jones	justingomez@ford-gomez.info	ep++j7BfHJ	37.6729148000000009	-122.385924500000002	8:15	trail
182	Michael Melton	julie52@mcmahon.com	$7jGl$$y$$	37.6645486000000034	-122.399010399999995	7:45	road
183	Kevin Cole	wattselizabeth@wilson.com	LSQzJeOM@9	37.6401206999999971	-122.414607599999997	9:15	both
184	Angela Brennan	tkelley@hotmail.com	M$g5W0xg&9	37.6520100687069004	-122.392942460239993	10:15	both
185	Jessica Johnson	justinjohns@gmail.com	k$H7x0om3A	37.6506808919823968	-122.387132829375005	6:00	both
186	William Berry	wendyoliver@williams.info	(hC1J49kr$	37.6413118080808005	-122.411514212121006	12:00	road
187	Douglas Morrow	wknight@yahoo.com	EQ)D8Fmth!	37.6428629999999984	-122.417769142856997	10:45	both
188	Jose Torres	kevinshea@richardson.com	##HAd4nX@Z	37.6525570816327004	-122.411133877550995	12:00	trail
189	Michael Rodgers	susanwebster@gmail.com	#&JmSdpS2o	37.5808284285714009	-122.347955591837007	10:00	road
190	Francisco Hanson	amontoya@yahoo.com	@X1Yz$bnei	37.5797853500000016	-122.350649516203006	10:45	road
191	Dale Foster	mgonzalez@yahoo.com	a0ZXARLv)x	37.5749018445916008	-122.342974709456001	11:00	both
192	Thomas Banks	watkinsdenise@white.info	1M3Cjmcm6&	37.5790178000000026	-122.348920827762996	6:00	both
193	Stacey Evans MD	mwhite@mccoy-huynh.net	*(2RSNPaVZ	37.5791709095137989	-122.346360073471004	7:30	both
194	Isabella Jackson	lindsayromero@reed-mclaughlin.com	y5Zl+Fme#2	37.5892728380648009	-122.342895225955004	7:45	road
197	Oren Leaffer	oren.leaffer@gmail.com	OrenL	37.5867873447243994	-122.343317235060994	9:45	trail
198	Austin Smith	austin.smith@gmail.com	Asmith	37.5867810458013025	-122.343081925291003	10:00	road
199	Meredyth Haas	Mhaas@gmail.com	Merber	37.5866183276659029	-122.343136303885004	10:00	road
200	Amanda Peterson	amanda.peterson@gmail.com	Apeterson	37.5867823055858992	-122.343128987244995	10:00	trail
201	Josh Leskar	jleskar@gmail.com	Jleskar	37.5867886045090032	-122.343364297015	10:00	road
202	Joanne Hutton	bonesifix@aol.com	jojo	37.5865939999999981	-122.335837999999995	10:00	both
203	Kate Orr	korr@gmail.com	KateO	37.5865670000000023	-122.334801999999996	9:30	trail
204	Jason Bourne	jbourne@cia.gov	Jason	37.5866221038008987	-122.343277549316994	9:45	trail
196	Kirby Hutton	kirby.hutton@gmail.com	ABC123	37.5866221038008987	-122.343277549316994	9:45	trail
205	Judith A. Gray	judithannegray@gmail.com	password	37.5867747468781985	-122.342846615520997	10:30	trail
\.


--
-- Name: messages_msg_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.messages_msg_id_seq', 26, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_id_seq', 205, true);


--
-- Name: compatibilities compatibilities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compatibilities
    ADD CONSTRAINT compatibilities_pkey PRIMARY KEY (user_id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (msg_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: compatibilities compatibilities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compatibilities
    ADD CONSTRAINT compatibilities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: messages messages_receiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_receiver_id_fkey FOREIGN KEY (receiver_id) REFERENCES public.users(user_id);


--
-- Name: messages messages_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(user_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

