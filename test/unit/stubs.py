import sys, os
sys.path.append("../../src")
os.environ["HULU_ENV"] = "test"

GOOD_STUBS = {
    "banya_geok_pair" : {
        "tracking_id" : "c0b47302d8ad8e503adb920bc14d2865",
        "raw_data" : None,
        "raw_app_data" : r'''
{"process": 27851, "levelname": "INFO", "name": "banya", "message": "user_view_count user_id: 2000086331, device: 1, playlist_device: 73, views_count: 0, client_ip_num: 3495664710, device_id: 1BDF1C345E033F0C79056F7E7D6F5E5E, add_block: None, add_is_extra_multi_view: False, total_views_count: 0", "service_name": "banya", "environment": {"datacenter": "els", "hostname": "els-ass-087", "name": "staging"}, "human_timestamp": "2016-03-14T21:42", "tracking_id": "c0b47302d8ad8e503adb920bc14d2865", "timestamp": 1458016928.674196, "span_id": "1", "category": "application"}
{"process": 27851, "levelname": "STATS", "name": "banya", "message": "adding view {'hits.token': 'tM3KIRQc', '_id': 2000086331}", "service_name": "banya", "environment": {"datacenter": "els", "hostname": "els-ass-087", "name": "staging"}, "human_timestamp": "2016-03-14T21:42", "tracking_id": "c0b47302d8ad8e503adb920bc14d2865", "timestamp": 1458016928.674438, "span_id": "1", "category": "application"}
{"process": 27851, "levelname": "INFO", "name": "src.tracking_id", "message": "completed request", "service_name": "banya", "environment": {"datacenter": "els", "hostname": "els-ass-087", "name": "staging"}, "human_timestamp": "2016-03-14T21:42", "tracking_id": "c0b47302d8ad8e503adb920bc14d2865", "timestamp": 1458016928.677775, "span_id": "1", "category": "aggregated", "context": {"events": [{"category": "request_start", "timestamp": 1458016928.630059, "context": {"body": {"rv": "790906", "guid": "1BDF1C345E033F0C79056F7E7D6F5E5E", "kv": "16875", "language": "en"}, "headers": {}, "url_full": "http://banya.staging.hulu.com/banya_playlist?vp=1&video_id=50153632&skip_ad_support=true&region=US&version=1&dp_id=hulu&pp=hulu&device_id=1BDF1C345E033F0C79056F7E7D6F5E5E&ad_ui_capable=true&device=73&x_redirect_header=X-Accel-Redirect&x_redirect=%2Fplaylist_end_track", "url_args": {}, "http_method": "POST", "url_host": "banya.staging.hulu.com", "url_path": "/banya_playlist"}}, {"category": "dependency_start", "timestamp": 1458016928.650321, "context": {"dependency_span_id": "1.1", "args": ["GET", "/user/2000086331"], "dependency_name": "kardashian", "kwargs": {}, "function_name": "_make_request"}}, {"category": "dependency_end", "timestamp": 1458016928.655745, "context": {"exception": false, "dependency_span_id": "1.1"}}, {"category": "dependency_start", "timestamp": 1458016928.663873, "context": {"dependency_span_id": "1.2", "args": ["GET", "/ip2geoinfo"], "dependency_name": "geok", "kwargs": {}, "function_name": "_make_request"}}, {"category": "dependency_end", "timestamp": 1458016928.669962, "context": {"exception": false, "dependency_span_id": "1.2"}}, {"category": "request_end", "timestamp": 1458016928.677702, "context": {"r_headers": {"X-Accel-Redirect": "/playlist_end_track?vp=1&package_id=2", "Content-type": "text/plain"}, "r_body": "OK", "r_exception": {"msg": null, "traceback": null}, "r_status": "200 OK"}}]}}
{"process": 24445, "levelname": "INFO", "name": "src.server.tracking_id", "message": "completed request", "service_name": "geok", "environment": {"datacenter": "els", "hostname": "els-ass-087", "name": "stage"}, "human_timestamp": "2016-03-14 21:42:08", "tracking_id": "c0b47302d8ad8e503adb920bc14d2865", "timestamp": 1458016928.668461, "span_id": "1.2", "category": "aggregated", "context": {"events": [{"category": "request_start", "timestamp": 1458016928.667579, "context": {"body": {}, "headers": {}, "url_full": "http://geok.els.staging.hulu.com/ip2geoinfo?ip=208.91.156.70&no_override=0&preferred_country=US&format=json", "url_args": {}, "http_method": "GET", "url_host": "geok.els.staging.hulu.com", "url_path": "/ip2geoinfo"}}, {"category": "request_end", "timestamp": 1458016928.668326, "context": {"r_headers": {"Content-type": "application/json"}, "r_body": "{\"country\": \"**\", \"anonpxy\": false}", "r_exception": {"msg": null, "traceback": null}, "r_status": "200 OK"}}]}}
''',
        "expected_zipkin_format" : [
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1458016928630059,
                "value": "sr"
            },
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1458016928677702,
                "value": "ss"
            }
        ],
        "binaryAnnotations": [
            {
                "key": "log_event_0",
                "value": "user_view_count user_id: 2000086331, device: 1, playlist_device: 73, views_count: 0, client_ip_num: 3495664710, device_id: 1BDF1C345E033F0C79056F7E7D6F5E5E, add_block: None, add_is_extra_multi_view: False, total_views_count: 0"
            },
            {
                "key": "log_event_1",
                "value": "adding view {'hits.token': 'tM3KIRQc', '_id': 2000086331}"
            },
            {
                "key": "body",
                "value": "{u'rv': u'790906', u'guid': u'1BDF1C345E033F0C79056F7E7D6F5E5E', u'kv': u'16875', u'language': u'en'}"
            },
            {
                "key": "url_args",
                "value": "{}"
            },
            {
                "key": "url_full",
                "value": "http://banya.staging.hulu.com/banya_playlist?vp=1&video_id=50153632&skip_ad_support=true&region=US&version=1&dp_id=hulu&pp=hulu&device_id=1BDF1C345E033F0C79056F7E7D6F5E5E&ad_ui_capable=true&device=73&x_redirect_header=X-Accel-Redirect&x_redirect=%2Fplaylist_end_track"
            },
            {
                "key": "headers",
                "value": "{}"
            },
            {
                "key": "http_method",
                "value": "POST"
            },
            {
                "key": "url_host",
                "value": "banya.staging.hulu.com"
            },
            {
                "key": "url_path",
                "value": "/banya_playlist"
            },
            {
                "key": "r_headers",
                "value": "{u'Content-type': u'text/plain', u'X-Accel-Redirect': u'/playlist_end_track?vp=1&package_id=2'}"
            },
            {
                "key": "r_status",
                "value": "200 OK"
            },
            {
                "key": "r_exception",
                "value": "{u'msg': None, u'traceback': None}"
            },
            {
                "key": "r_body",
                "value": "OK"
            }
        ],
        "duration": 47643,
        "id": "1",
        "name": "banya",
        "timestamp": 1458016928630059,
        "traceId": "c0b47302d8ad8e503adb920bc14d2865"
    },
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1458016928663873,
                "value": "cs"
            },
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1458016928669962,
                "value": "cr"
            },
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1458016928667578,
                "value": "sr"
            },
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1458016928668326,
                "value": "ss"
            }
        ],
        "binaryAnnotations": [
            {
                "key": "body",
                "value": "{}"
            },
            {
                "key": "url_args",
                "value": "{}"
            },
            {
                "key": "url_full",
                "value": "http://geok.els.staging.hulu.com/ip2geoinfo?ip=208.91.156.70&no_override=0&preferred_country=US&format=json"
            },
            {
                "key": "headers",
                "value": "{}"
            },
            {
                "key": "http_method",
                "value": "GET"
            },
            {
                "key": "url_host",
                "value": "geok.els.staging.hulu.com"
            },
            {
                "key": "url_path",
                "value": "/ip2geoinfo"
            },
            {
                "key": "r_headers",
                "value": "{u'Content-type': u'application/json'}"
            },
            {
                "key": "r_status",
                "value": "200 OK"
            },
            {
                "key": "r_exception",
                "value": "{u'msg': None, u'traceback': None}"
            },
            {
                "key": "r_body",
                "value": "{\"country\": \"**\", \"anonpxy\": false}"
            }
        ],
        "duration": 6089,
        "id": "1.2",
        "name": "geok",
        "timestamp": 1458016928663873,
        "traceId": "c0b47302d8ad8e503adb920bc14d2865"
    },
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1458016928650321,
                "value": "cs"
            },
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1458016928655745,
                "value": "cr"
            }
        ],
        "binaryAnnotations": [],
        "duration": 5424,
        "id": "1.1",
        "name": "kardashian",
        "timestamp": 1458016928650321,
        "traceId": "c0b47302d8ad8e503adb920bc14d2865"
    }
],

        "expected_hulu_format" : [
    {
        "label": "banya application call",
        "times": [
            {
                "ending_time": 1458016928677,
                "label": "47.64 ms",
                "starting_time": 1458016928630
            }
        ]
    },
    {
        "label": "geok application call",
        "times": [
            {
                "ending_time": 1458016928668,
                "label": "0.746 ms",
                "starting_time": 1458016928667
            }
        ]
    },
    {
        "label": "banya dependency call",
        "times": [
            {
                "ending_time": 1458016928655,
                "label": "kardashian | 5.424 ms",
                "starting_time": 1458016928650
            }
        ]
    },
    {
        "label": "banya dependency call",
        "times": [
            {
                "ending_time": 1458016928669,
                "label": "geok | 6.088 ms",
                "starting_time": 1458016928663
            }
        ]
    }
]
    },

    "geok_ip2_geoinfo" : {
        "tracking_id" : "63086ac2b4b0e59b18ff709bd6cc782b",
        "raw_data" : None,
        "raw_app_data" : r'''
{"process": 77634, "levelname": "INFO", "name": "src.server.tracking_id", "message": "starting request", "category": "request_start", "service_name": "geok", "human_timestamp": "2016-03-04 00:26:53", "tracking_id": "63086ac2b4b0e59b18ff709bd6cc782b", "timestamp": 1457080013.196157, "span_id": "1", "context": {"body": {}, "header": {"Accept-Language": "en-US,en;q=0.8", "Accept-Encoding": "gzip, deflate, sdch", "Host": "local.hulu.com:7007", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Upgrade-Insecure-Requests": "1", "Dnt": "1", "Connection": "keep-alive", "Cookie": "optimizelyEndUserId=oeu1452296903073r0.9307221733033657; fbm_40582213222=base_domain=.hulu.com; _hp2_id.2418515605=5972134801320682.0219404225.3238809154; _ga=GA1.2.393771461.1452296905; fblo_40582213222=y; _hulu_session=UWUgRAJxegqagpr-ObTpGQ; _hulu_uid=17100968; _hulu_e_uid=7BSWsJwlJSzQQZucrhR_IQ; _hulu_su=10C6BC69-1889-3A4A-C8F5-F01D05BA825F; _driver_page=favorites; _driver_type=other; _driver_id_1=; _driver_id_2=; _driver_id_3=; _upsell_type=; hulu_sso_data=H4sIACG72FYC_21XbW8aORD-K1E-dyNCkvYaqdJRoA1teRFLklank2V2B3Ax9tb2QrjT_feb8b7Y0Hxi8cu8PvPM-N_LXF3eX1z2Jx96SsiLJy6c5G-mjx_0aiUyYClXjo-1EplffbRgPnILbwb9D5k2Bf1uSllW_3eXby4uSzyi-A5ILEeZV3svk7YyKUA5Jgrau-5cda5u319dd7q0J7l1rLn31F5ZG10WFtf-uhwMZ9-mP9jDYjqjnc_c8DX08p1Qlv4PYG9ZOqbPPpd8ye2GvvNMFzY5cKOEWvuD_Rkb5sJpE65NC7sA7s2fz7osdXyNp_11ZXkhEjCmPr8p1-B0kXAJxtHCA7q_B2OBYuOPZFo5ocpyF10bKQdmL-DgTRfuGZa9LAPrN-Elg8IJrWyyFWqraW3HhVzqY6K0E5gJTtveXp2vYcmlDJ6jyX5nks60cVx6Q5h2GzBe0tH-kskOwJUF_Z-AO2izRccxwd80ekqrXw3fgv96mk1uWE9KtjCcQOBl9zFE9DHjRsJxzLONUDDmClPglTwLleuDjdJRZevraPJ16uP2ixFQ1rzaLi1zdcSnBl0LF79h6F7C3xqHZRNcjJ23OZxNy1xDlMxPpZROIJA8EmwBJk5oG6WgAqMhcy_uY8gJohuS41l2llwdeeTd995sxGbz6eCxvxhNJx4OowWrw2OZ11GhRpaJ1SjdR8vmNslhT58ply5KJVi3KiU62aJpRiHOS3dk7VKlfThng-HwS-8HLX2SKjesn_bYY-p9qgEfTM51USBmkzaSfYQpliO6ECKVoARvIJX9zpf9qg4n7AqpjwBV4LlQAs4MYuPHyefhvLovXdA0qFQPwEs40c7mQFXRHFQRggi_WGbSGw_78zI-g7sBX4Te9zwyv76drEG_covywmriQtyfw37DTZ54JPhy93p7cmUgnwPPp0p6gPiabfJJutqYW6r5DJQ-JKSp8tvAgDvip4i8MqPVVjDe4AUZF44LAxAlfTp5XLBevz9M0zbj9PERY3TcaB3xDxrcVFeE3joEvmhCDdld9_auU4HUlUtgETBD6E9hN-_NqjxjjubJrFxKYWu2QXYNbkXKEfJ-25R5o6FGzZfxdzaeTkaL6Txl82G6OIl8zLn1PQplrpEgKyU5ha7Z24EzIsPEin1EGv1x-lpt1AHpbxAna_1JSEhRL7D5c-gcQq30Ce-2Ya4pL0SyBmkg_T5Xex4h-pvOYt4ZkOERh25EkW24S_RBVQs5wE9-bFw7g24OO10B-BdvIPwaun960q86nuASY8ACy30ZzXsKS3ElS1AZvJq5ygpaNMhO1A1rg-ZQoDKMZJCX62yLVVsfIKw_8FzrIgje7M-Kk_pn03zpwlRlddH7S8I6w5tmbXco2UWdemZ0XtWPcChPhjJd-_GgsYRqe-o7id8DvW12soKthOIqa6jj95L9AVLqQ4Hiolz21nwPU6TM1rjnLUbHh-wiHGsGpmgJNR7Q3Lo_FTotUUrob9ysBFT9SFUNM8PZyHbe1fDe4FHJNxG4UUYLyjE4soI9BVLNKqZNaL20ifFZ8zsPegf_BNpAuS3WTLnn7Y7d6S0UmOiIBlOdnxKO0twPXBZdqwmjakpV0aWQlej1MR19pr_EORRf3SbF9-4FIuxVcs-Fgcyd0tBo3Bv_TnFbWnqJYDqBl9I-nnU9Nqg2kWh5FsKHTgKnZtVcPgNrpGqlzRoCT4Sqr50n_mzlfinVWsJA2G1aLttVjGHEBr_XbijspnkH_RHhNBRFBGYYSNhzBx5At9cd1tZi5XdN1pjMGCN00BIOPayqSnBNLmJGP-Q5QaMF3yccUz9KvW4nnTBVsGdCee2_izngaTSrWl1VSY7wLbhKAhG1qGoK2zebo8FKDMD_odGP0CCj3BCUfTHpkwgjwk74PzBb1mqO5yMDDTEtDjQ-7wKMcEJ7lSwzT_lNHTQowpGCclPl1_tMwxaP4loNVOG_RVZBwmkHglN0VLyp1ub4EM3URHLDeEpDIzflckhPj8KIeN6oJ7J64e-6qTJrNdvCkYncv9A8mpc_sfA-P44GtJStujed65u75G12e5fc3l2_T97f5HnCs7ucZ7fdd7dLP0rsuRQ5cwKJHG91O9dvk85N0rm9uP7j_qZzf_euCrp1yLRonX-CpotO94872lgJEz0G6WEaZK4MVkQs8-ai273v3tUypa6fSvdUgVi7F-NoDCy4cTvUSLsLyDZKI3SrIZ_eW2dP1j8pJldUgf_9DzsPtXUoDwAA; hulu_sso_sig=x9bgZDkPfWzWbLSl1KlvobnGvPbXAdJm-BX5VJjuaWQe1JgdI_nHwzC82UdBwKXcSM8WeYnvtplnajCJwUwqsQBF9HDqcQukRfLF2Yka2DKWM9X9z-JG0Oaq80WK-HmP2PBH0xzLBuDCl8Oo01-lUF7c6Eyw_3VBXNwpmjmkYlTZ3384cnGFLeJwIIZODkyMX0PvFTMAuvEgaX0BX_MHXX3V6JvZs6wWpda4JvPigWhI56Da_7xk7VYQnQhJ_jwWzPxmH8LCYxlJ7Ai7GqqBkbU9ZoiXkbwajlgeb6Kj2173M91JkVJaOQLSbqoWzA_S4vSlZWiuYXs2TgFnouptHg==; _ue=1457045680; _hulu_hbc=1457045679826; hic=1; _hulu_uname=Zheng; _hoa=true; _hob=true; _wyw_sort=1; _hulu_pgid=1; _hulu_plid=262144; _hulu_psh=0; _hulu_psvh=0; _hulu_qc=1279; _hulu_fc=16; _hulu_bluekai_hashed_uid=4ce4fa19eb28e2d58594a32a13a6f70a; _hulu_wlv2_optin=-1; optimizelySegments=%7B%223553151460%22%3A%22referral%22%2C%223571650242%22%3A%22gc%22%2C%223573441101%22%3A%22false%22%2C%223688050120%22%3A%22none%22%7D; guid=BCECCB14EE91602C9C8A19C101FF9CA8; locale=en; _rcsources=watch%7C%7Cblank%7Creferral%7C%7C; optimizelyBuckets=%7B%7D; _hulu_auth2=; __utma=155684772.393771461.1452296905.1456883679.1457045680.23; __utmc=155684772; __utmz=155684772.1452296905.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155684772.|1=login%20status=loggedin=1^3=h2o-treatment=control=1^5=h2o-treatment-web-guid-only=dope_roadblock%20-%20dope_w_signup_skip_lp=1^6=DonutTreatment=control=1^7=DonutTreatmentWebGuidOnly=dope_roadblock%20-%20dope_w_signup_skip_lp=1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"}, "param": {"ip": "50.112.0.0"}}}
{"process": 77634, "levelname": "INFO", "name": "src.server.server", "message": "anonymous ip block for 846200832 : 50.112.0.0", "category": "application", "service_name": "geok", "human_timestamp": "2016-03-04 00:26:53", "tracking_id": "63086ac2b4b0e59b18ff709bd6cc782b", "timestamp": 1457080013.198636, "span_id": "1"}
{"process": 77634, "levelname": "INFO", "name": "src.server.tracking_id", "message": "ending request", "category": "request_end", "service_name": "geok", "human_timestamp": "2016-03-04 00:26:53", "tracking_id": "63086ac2b4b0e59b18ff709bd6cc782b", "timestamp": 1457080013.201488, "span_id": "1", "context": {}}
''',
        "expected_zipkin_format" : [
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457080013196157,
                "value": "sr"
            },
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457080013201488,
                "value": "ss"
            }
        ],
        "binaryAnnotations": [
            {
                "key": "body",
                "value": "{}"
            },
            {
                "key": "header",
                "value": "{u'Accept-Language': u'en-US,en;q=0.8', u'Accept-Encoding': u'gzip, deflate, sdch', u'Connection': u'keep-alive', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', u'Upgrade-Insecure-Requests': u'1', u'Dnt': u'1', u'Host': u'local.hulu.com:7007', u'Cookie': u'optimizelyEndUserId=oeu1452296903073r0.9307221733033657; fbm_40582213222=base_domain=.hulu.com; _hp2_id.2418515605=5972134801320682.0219404225.3238809154; _ga=GA1.2.393771461.1452296905; fblo_40582213222=y; _hulu_session=UWUgRAJxegqagpr-ObTpGQ; _hulu_uid=17100968; _hulu_e_uid=7BSWsJwlJSzQQZucrhR_IQ; _hulu_su=10C6BC69-1889-3A4A-C8F5-F01D05BA825F; _driver_page=favorites; _driver_type=other; _driver_id_1=; _driver_id_2=; _driver_id_3=; _upsell_type=; hulu_sso_data=H4sIACG72FYC_21XbW8aORD-K1E-dyNCkvYaqdJRoA1teRFLklank2V2B3Ax9tb2QrjT_feb8b7Y0Hxi8cu8PvPM-N_LXF3eX1z2Jx96SsiLJy6c5G-mjx_0aiUyYClXjo-1EplffbRgPnILbwb9D5k2Bf1uSllW_3eXby4uSzyi-A5ILEeZV3svk7YyKUA5Jgrau-5cda5u319dd7q0J7l1rLn31F5ZG10WFtf-uhwMZ9-mP9jDYjqjnc_c8DX08p1Qlv4PYG9ZOqbPPpd8ye2GvvNMFzY5cKOEWvuD_Rkb5sJpE65NC7sA7s2fz7osdXyNp_11ZXkhEjCmPr8p1-B0kXAJxtHCA7q_B2OBYuOPZFo5ocpyF10bKQdmL-DgTRfuGZa9LAPrN-Elg8IJrWyyFWqraW3HhVzqY6K0E5gJTtveXp2vYcmlDJ6jyX5nks60cVx6Q5h2GzBe0tH-kskOwJUF_Z-AO2izRccxwd80ekqrXw3fgv96mk1uWE9KtjCcQOBl9zFE9DHjRsJxzLONUDDmClPglTwLleuDjdJRZevraPJ16uP2ixFQ1rzaLi1zdcSnBl0LF79h6F7C3xqHZRNcjJ23OZxNy1xDlMxPpZROIJA8EmwBJk5oG6WgAqMhcy_uY8gJohuS41l2llwdeeTd995sxGbz6eCxvxhNJx4OowWrw2OZ11GhRpaJ1SjdR8vmNslhT58ply5KJVi3KiU62aJpRiHOS3dk7VKlfThng-HwS-8HLX2SKjesn_bYY-p9qgEfTM51USBmkzaSfYQpliO6ECKVoARvIJX9zpf9qg4n7AqpjwBV4LlQAs4MYuPHyefhvLovXdA0qFQPwEs40c7mQFXRHFQRggi_WGbSGw_78zI-g7sBX4Te9zwyv76drEG_covywmriQtyfw37DTZ54JPhy93p7cmUgnwPPp0p6gPiabfJJutqYW6r5DJQ-JKSp8tvAgDvip4i8MqPVVjDe4AUZF44LAxAlfTp5XLBevz9M0zbj9PERY3TcaB3xDxrcVFeE3joEvmhCDdld9_auU4HUlUtgETBD6E9hN-_NqjxjjubJrFxKYWu2QXYNbkXKEfJ-25R5o6FGzZfxdzaeTkaL6Txl82G6OIl8zLn1PQplrpEgKyU5ha7Z24EzIsPEin1EGv1x-lpt1AHpbxAna_1JSEhRL7D5c-gcQq30Ce-2Ya4pL0SyBmkg_T5Xex4h-pvOYt4ZkOERh25EkW24S_RBVQs5wE9-bFw7g24OO10B-BdvIPwaun960q86nuASY8ACy30ZzXsKS3ElS1AZvJq5ygpaNMhO1A1rg-ZQoDKMZJCX62yLVVsfIKw_8FzrIgje7M-Kk_pn03zpwlRlddH7S8I6w5tmbXco2UWdemZ0XtWPcChPhjJd-_GgsYRqe-o7id8DvW12soKthOIqa6jj95L9AVLqQ4Hiolz21nwPU6TM1rjnLUbHh-wiHGsGpmgJNR7Q3Lo_FTotUUrob9ysBFT9SFUNM8PZyHbe1fDe4FHJNxG4UUYLyjE4soI9BVLNKqZNaL20ifFZ8zsPegf_BNpAuS3WTLnn7Y7d6S0UmOiIBlOdnxKO0twPXBZdqwmjakpV0aWQlej1MR19pr_EORRf3SbF9-4FIuxVcs-Fgcyd0tBo3Bv_TnFbWnqJYDqBl9I-nnU9Nqg2kWh5FsKHTgKnZtVcPgNrpGqlzRoCT4Sqr50n_mzlfinVWsJA2G1aLttVjGHEBr_XbijspnkH_RHhNBRFBGYYSNhzBx5At9cd1tZi5XdN1pjMGCN00BIOPayqSnBNLmJGP-Q5QaMF3yccUz9KvW4nnTBVsGdCee2_izngaTSrWl1VSY7wLbhKAhG1qGoK2zebo8FKDMD_odGP0CCj3BCUfTHpkwgjwk74PzBb1mqO5yMDDTEtDjQ-7wKMcEJ7lSwzT_lNHTQowpGCclPl1_tMwxaP4loNVOG_RVZBwmkHglN0VLyp1ub4EM3URHLDeEpDIzflckhPj8KIeN6oJ7J64e-6qTJrNdvCkYncv9A8mpc_sfA-P44GtJStujed65u75G12e5fc3l2_T97f5HnCs7ucZ7fdd7dLP0rsuRQ5cwKJHG91O9dvk85N0rm9uP7j_qZzf_euCrp1yLRonX-CpotO94872lgJEz0G6WEaZK4MVkQs8-ai273v3tUypa6fSvdUgVi7F-NoDCy4cTvUSLsLyDZKI3SrIZ_eW2dP1j8pJldUgf_9DzsPtXUoDwAA; hulu_sso_sig=x9bgZDkPfWzWbLSl1KlvobnGvPbXAdJm-BX5VJjuaWQe1JgdI_nHwzC82UdBwKXcSM8WeYnvtplnajCJwUwqsQBF9HDqcQukRfLF2Yka2DKWM9X9z-JG0Oaq80WK-HmP2PBH0xzLBuDCl8Oo01-lUF7c6Eyw_3VBXNwpmjmkYlTZ3384cnGFLeJwIIZODkyMX0PvFTMAuvEgaX0BX_MHXX3V6JvZs6wWpda4JvPigWhI56Da_7xk7VYQnQhJ_jwWzPxmH8LCYxlJ7Ai7GqqBkbU9ZoiXkbwajlgeb6Kj2173M91JkVJaOQLSbqoWzA_S4vSlZWiuYXs2TgFnouptHg==; _ue=1457045680; _hulu_hbc=1457045679826; hic=1; _hulu_uname=Zheng; _hoa=true; _hob=true; _wyw_sort=1; _hulu_pgid=1; _hulu_plid=262144; _hulu_psh=0; _hulu_psvh=0; _hulu_qc=1279; _hulu_fc=16; _hulu_bluekai_hashed_uid=4ce4fa19eb28e2d58594a32a13a6f70a; _hulu_wlv2_optin=-1; optimizelySegments=%7B%223553151460%22%3A%22referral%22%2C%223571650242%22%3A%22gc%22%2C%223573441101%22%3A%22false%22%2C%223688050120%22%3A%22none%22%7D; guid=BCECCB14EE91602C9C8A19C101FF9CA8; locale=en; _rcsources=watch%7C%7Cblank%7Creferral%7C%7C; optimizelyBuckets=%7B%7D; _hulu_auth2=; __utma=155684772.393771461.1452296905.1456883679.1457045680.23; __utmc=155684772; __utmz=155684772.1452296905.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=155684772.|1=login%20status=loggedin=1^3=h2o-treatment=control=1^5=h2o-treatment-web-guid-only=dope_roadblock%20-%20dope_w_signup_skip_lp=1^6=DonutTreatment=control=1^7=DonutTreatmentWebGuidOnly=dope_roadblock%20-%20dope_w_signup_skip_lp=1', u'User-Agent': u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}"
            },
            {
                "key": "param",
                "value": "{u'ip': u'50.112.0.0'}"
            },
            {
                "key": "log_event_1",
                "value": "anonymous ip block for 846200832 : 50.112.0.0"
            }
        ],
        "duration": 5331,
        "id": "1",
        "name": "geok",
        "timestamp": 1457080013196157,
        "traceId": "63086ac2b4b0e59b18ff709bd6cc782b"
    }
],
        "expected_hulu_format" : [
    {
        "label": "geok application call",
        "times": [
            {
                "ending_time": 1457080013201,
                "label": "5.331 ms",
                "starting_time": 1457080013196
            }
        ]
    }
],
    },

    "geok_ip2_geoinfo_aggregated" : {
        "tracking_id" : "27ae0a192961f16ec743e7a321512fe0",
        "raw_data" : None,
        "raw_app_data" : r'''
{"process": 13363, "levelname": "INFO", "name": "src.server.tracking_id", "message": "completed request", "service_name": "geok", "environment": {"datacenter": "els", "hostname": "MACBOXYCFH04", "name": "prod"}, "human_timestamp": "2016-03-10 00:02:39", "tracking_id": "27ae0a192961f16ec743e7a321512fe0", "timestamp": 1457596959.695487, "span_id": "1", "category": "aggregated", "context": {"events": [{"category": "request_start", "timestamp": 1457596959.694225, "context": {"body": {}, "headers": {}, "url_full": "http://local.hulu.com:7007/ip2geoinfo?ip=50.112.0.0", "url_args": {"ip": "50.112.0.0"}, "http_method": "GET", "url_host": "local.hulu.com:7007", "url_path": "/ip2geoinfo"}}, {"category": "request_end", "timestamp": 1457596959.695382, "context": {"status": "200 OK", "headers": [["Content-type", "application/json"]], "exception": {"msg": null, "traceback": null}, "body": "{\"country\": \"us\", \"anonpxy\": true}"}}]}}
''',
        "expected_zipkin_format" : [
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457596959694225,
                "value": "sr"
            },
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457596959695382,
                "value": "ss"
            }
        ],
        "binaryAnnotations": [
            {
                "key": "body",
                "value": "{}"
            },
            {
                "key": "url_args",
                "value": "{u'ip': u'50.112.0.0'}"
            },
            {
                "key": "url_full",
                "value": "http://local.hulu.com:7007/ip2geoinfo?ip=50.112.0.0"
            },
            {
                "key": "headers",
                "value": "{}"
            },
            {
                "key": "http_method",
                "value": "GET"
            },
            {
                "key": "url_host",
                "value": "local.hulu.com:7007"
            },
            {
                "key": "url_path",
                "value": "/ip2geoinfo"
            },
            {
                "key": "status",
                "value": "200 OK"
            },
            {
                "key": "headers",
                "value": "[[u'Content-type', u'application/json']]"
            },
            {
                "key": "exception",
                "value": "{u'msg': None, u'traceback': None}"
            },
            {
                "key": "body",
                "value": "{\"country\": \"us\", \"anonpxy\": true}"
            }
        ],
        "duration": 1157,
        "id": "1",
        "name": "geok",
        "timestamp": 1457596959694225,
        "traceId": "27ae0a192961f16ec743e7a321512fe0"
    }
],
        "expected_hulu_format" : [
    {
        "label": "geok application call",
        "times": [
            {
                "ending_time": 1457596959695,
                "label": "1.157 ms",
                "starting_time": 1457596959694
            }
        ]
    }
],
    },

    "geok_db_data_aggregated" : {
        "tracking_id" : "ec962739b524115bb5f64be2549cf7ed",
        "raw_data" : None,
        "raw_app_data": r'''
{"process": 13363, "levelname": "INFO", "name": "src.server.tracking_id", "message": "completed request", "service_name": "geok", "environment": {"datacenter": "els", "hostname": "MACBOXYCFH04", "name": "prod"}, "human_timestamp": "2016-03-10 00:11:30", "tracking_id": "ec962739b524115bb5f64be2549cf7ed", "timestamp": 1457597490.088879, "span_id": "1", "category": "aggregated", "context": {"events": [{"category": "request_start", "timestamp": 1457597488.457631, "context": {"body": {}, "headers": {}, "url_full": "http://local.hulu.com:7007/fetch_db_info", "url_args": {}, "http_method": "GET", "url_host": "local.hulu.com:7007", "url_path": "/fetch_db_info"}}, {"category": "dependency_start", "timestamp": 1457597488.457912, "context": {"dependency_name": "ther", "args": ["country"], "dependency_span_id": "1.1", "kwargs": {}, "function_name": "get_overrides_from_db"}}, {"category": "dependency_end", "timestamp": 1457597489.233482, "context": {"exception": false, "dependency_span_id": "1.1"}}, {"category": "dependency_start", "timestamp": 1457597489.233597, "context": {"dependency_name": "ther", "args": ["city"], "dependency_span_id": "1.2", "kwargs": {}, "function_name": "get_overrides_from_db"}}, {"category": "dependency_end", "timestamp": 1457597489.349697, "context": {"exception": false, "dependency_span_id": "1.2"}}, {"category": "dependency_start", "timestamp": 1457597489.349897, "context": {"dependency_name": "ther", "args": ["postal"], "dependency_span_id": "1.3", "kwargs": {}, "function_name": "get_overrides_from_db"}}, {"category": "dependency_end", "timestamp": 1457597489.476603, "context": {"exception": false, "dependency_span_id": "1.3"}}, {"category": "dependency_start", "timestamp": 1457597489.476823, "context": {"dependency_name": "ther", "args": ["ip_block_whitelist"], "dependency_span_id": "1.4", "kwargs": {}, "function_name": "get_overrides_from_db"}}, {"category": "dependency_end", "timestamp": 1457597489.853487, "context": {"exception": false, "dependency_span_id": "1.4"}}, {"category": "dependency_start", "timestamp": 1457597489.853605, "context": {"dependency_name": "ther", "args": ["ip_block_blacklist"], "dependency_span_id": "1.5", "kwargs": {}, "function_name": "get_overrides_from_db"}}, {"category": "dependency_end", "timestamp": 1457597489.992757, "context": {"exception": false, "dependency_span_id": "1.5"}}, {"category": "request_end", "timestamp": 1457597490.088677, "context": {"status": "200 OK", "headers": [["Content-type", "application/json"]], "exception": {"msg": null, "traceback": null}, "body": "{\"country\": {\"data\": [{\"country\": \"us\", \"cidr\": [16909060, 4294967295], \"ip_range\": \"1.2.3.4\"}, {\"country\": \"us\", \"cidr\": [41130334, 4294967295], \"ip_range\": \"2.115.153.94\"}, {\"country\": \"us\", \"cidr\": [68976902, 4294967295], \"ip_range\": \"4.28.129.6\"}, {\"country\": \"us\", \"cidr\": [69089290, 4294967295], \"ip_range\": \"4.30.56.10\"}, {\"country\": \"us\", \"cidr\": [69099654, 4294967295], \"ip_range\": \"4.30.96.134\"}, {\"country\": \"**\", \"cidr\": [69166026, 4294967295], \"ip_range\": \"4.31.99.202\"}, {\"country\": \"us\", \"cidr\": [72349104, 4294967295], \"ip_range\": \"4.79.245.176\"}, {\"country\": \"jp\", \"cidr\": [84345142, 4294967295], \"ip_range\": \"5.7.1.54\"}, {\"country\": \"us\", \"cidr\": [90251312, 4294967280], \"ip_range\": \"5.97.32.48/28\"}, {\"country\": \"us\", \"cidr\": [132222546, 4294967295], \"ip_range\": \"7.225.142.82\"}, {\"country\": \"us\", \"cidr\": [135530581, 4294967295], \"ip_range\": \"8.20.8.85\"}, {\"country\": \"us\", \"cidr\": [135530585, 4294967295], \"ip_range\": \"8.20.8.89\"}, {\"country\": \"us\", \"cidr\": [135530599, 429496729"}}]}}
''',
        "expected_zipkin_format" : [
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597488457631,
                "value": "sr"
            },
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597490088677,
                "value": "ss"
            }
        ],
        "binaryAnnotations": [
            {
                "key": "body",
                "value": "{}"
            },
            {
                "key": "url_args",
                "value": "{}"
            },
            {
                "key": "url_full",
                "value": "http://local.hulu.com:7007/fetch_db_info"
            },
            {
                "key": "headers",
                "value": "{}"
            },
            {
                "key": "http_method",
                "value": "GET"
            },
            {
                "key": "url_host",
                "value": "local.hulu.com:7007"
            },
            {
                "key": "url_path",
                "value": "/fetch_db_info"
            },
            {
                "key": "status",
                "value": "200 OK"
            },
            {
                "key": "headers",
                "value": "[[u'Content-type', u'application/json']]"
            },
            {
                "key": "exception",
                "value": "{u'msg': None, u'traceback': None}"
            },
            {
                "key": "body",
                "value": "{\"country\": {\"data\": [{\"country\": \"us\", \"cidr\": [16909060, 4294967295], \"ip_range\": \"1.2.3.4\"}, {\"country\": \"us\", \"cidr\": [41130334, 4294967295], \"ip_range\": \"2.115.153.94\"}, {\"country\": \"us\", \"cidr\": [68976902, 4294967295], \"ip_range\": \"4.28.129.6\"}, {\"country\": \"us\", \"cidr\": [69089290, 4294967295], \"ip_range\": \"4.30.56.10\"}, {\"country\": \"us\", \"cidr\": [69099654, 4294967295], \"ip_range\": \"4.30.96.134\"}, {\"country\": \"**\", \"cidr\": [69166026, 4294967295], \"ip_range\": \"4.31.99.202\"}, {\"country\": \"us\", \"cidr\": [72349104, 4294967295], \"ip_range\": \"4.79.245.176\"}, {\"country\": \"jp\", \"cidr\": [84345142, 4294967295], \"ip_range\": \"5.7.1.54\"}, {\"country\": \"us\", \"cidr\": [90251312, 4294967280], \"ip_range\": \"5.97.32.48/28\"}, {\"country\": \"us\", \"cidr\": [132222546, 4294967295], \"ip_range\": \"7.225.142.82\"}, {\"country\": \"us\", \"cidr\": [135530581, 4294967295], \"ip_range\": \"8.20.8.85\"}, {\"country\": \"us\", \"cidr\": [135530585, 4294967295], \"ip_range\": \"8.20.8.89\"}, {\"country\": \"us\", \"cidr\": [135530599, 429496729"
            }
        ],
        "duration": 1631046,
        "id": "1",
        "name": "geok",
        "timestamp": 1457597488457631,
        "traceId": "ec962739b524115bb5f64be2549cf7ed"
    },
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597489476823,
                "value": "cs"
            },
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597489853487,
                "value": "cr"
            }
        ],
        "binaryAnnotations": [],
        "duration": 376664,
        "id": "1.4",
        "name": "ther",
        "timestamp": 1457597489476823,
        "traceId": "ec962739b524115bb5f64be2549cf7ed"
    },
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597489853605,
                "value": "cs"
            },
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597489992757,
                "value": "cr"
            }
        ],
        "binaryAnnotations": [],
        "duration": 139152,
        "id": "1.5",
        "name": "ther",
        "timestamp": 1457597489853605,
        "traceId": "ec962739b524115bb5f64be2549cf7ed"
    },
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597488457911,
                "value": "cs"
            },
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597489233482,
                "value": "cr"
            }
        ],
        "binaryAnnotations": [],
        "duration": 775571,
        "id": "1.1",
        "name": "ther",
        "timestamp": 1457597488457911,
        "traceId": "ec962739b524115bb5f64be2549cf7ed"
    },
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597489233597,
                "value": "cs"
            },
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597489349697,
                "value": "cr"
            }
        ],
        "binaryAnnotations": [],
        "duration": 116100,
        "id": "1.2",
        "name": "ther",
        "timestamp": 1457597489233597,
        "traceId": "ec962739b524115bb5f64be2549cf7ed"
    },
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597489349897,
                "value": "cs"
            },
            {
                "endpoint": {
                    "ipv4": "geok",
                    "port": 0,
                    "serviceName": "geok"
                },
                "timestamp": 1457597489476603,
                "value": "cr"
            }
        ],
        "binaryAnnotations": [],
        "duration": 126706,
        "id": "1.3",
        "name": "ther",
        "timestamp": 1457597489349897,
        "traceId": "ec962739b524115bb5f64be2549cf7ed"
    }
],
    },

    "banya_playlist" : {
        "tracking_id" : "9bce2141f85f64e4710090211b6bb39e",
        "raw_data" : None,
        "raw_app_data" : r'''
{"process": 1217, "levelname": "INFO", "name": "banya", "message": "starting request", "category": "request_start", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.063047, "span_id": "1", "context": {"body": {}, "header": {"Host": "local.hulu.com:7986", "Accept": "*/*", "User-Agent": "curl/7.43.0"}, "param": {"x_redirect_header": "X-Accel-Redirect", "x_redirect": "/playlist_end", "video_id": "60516836", "token": "okNWazHAdddIcV0C2kvRXQ", "version": "3", "device": "6", "device_id": "h99b70153-1b34-7cda-8939-f09603243eb1"}}}
{"process": 1217, "levelname": "STATS", "name": "hulu.pyseal", "message": "no cached service token, request a new one", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.066158, "span_id": "1"}
{"process": 1217, "levelname": "STATS", "name": "hulu.pyseal", "message": "send request. endpoint: GetServiceToken, POST https://tut.test.hulu.com:8395/service/token/secret", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.066816, "span_id": "1"}
{"process": 1217, "levelname": "INFO", "name": "urllib3.connectionpool", "message": "Starting new HTTPS connection (1): tut.test.hulu.com", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.068978, "span_id": "1"}
{"process": 1217, "levelname": "STATS", "name": "urllib3.connectionpool", "message": "\"POST /service/token/secret HTTP/1.1\" 200 274", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.200349, "span_id": "1"}
{"process": 1217, "levelname": "STATS", "name": "hulu.pyseal", "message": "request service token successfully", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.203418, "span_id": "1"}
{"process": 1217, "levelname": "STATS", "name": "hulu.pyseal", "message": "send request. endpoint: CheckUserToken, GET https://tut.test.hulu.com:8395/user/check", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.204216, "span_id": "1"}
{"process": 1217, "levelname": "STATS", "name": "urllib3.connectionpool", "message": "\"GET /user/check?old_token=True&user_token=okNWazHAdddIcV0C2kvRXQ&hulu_session=False&service_token=lh07WnYChUO_WIqwQ9nmrYIw%2F2E-QlNmF_b96DsKM4ONgS7y7Q--wY9upC50ievKJEP_NZGjQaATKFwpODmCHNtLEWD3BRhyrDxtctabY3eXgB6bNUmQ6otdQN8XBRN18Eb%2FV39_ZQ6lRVZkCFLgirzcB3PZJ2o- HTTP/1.1\" 200 22", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.226886, "span_id": "1"}
{"process": 1217, "levelname": "STATS", "name": "hulu.pyseal", "message": "request duration: 23", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.228618, "span_id": "1"}
{"process": 1217, "levelname": "INFO", "name": "banya", "message": null, "category": "dependency_start", "context": {"dependency_span_id": "1.1", "args": ["GET", "/user/2000046631"], "dependency_name": "kardashian", "kwargs": {}, "function_name": "_make_request"}, "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.230686, "span_id": "1"}
{"process": 1217, "levelname": "INFO", "name": "urllib3.connectionpool", "message": "Starting new HTTP connection (1): kardashian.staging.hulu.com", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.231788, "span_id": "1"}
{"process": 1217, "levelname": "STATS", "name": "urllib3.connectionpool", "message": "\"GET /user/2000046631 HTTP/1.1\" 200 292", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.3048, "span_id": "1"}
{"process": 1217, "levelname": "INFO", "name": "banya", "message": null, "category": "dependency_end", "context": {"dependency_span_id": "1.1", "dependency_name": "kardashian", "function_name": "_make_request"}, "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.308684, "span_id": "1"}
{"process": 1217, "levelname": "INFO", "name": "banya", "message": "Redis Cache miss bya_vid_60516836_US, query time 0.134 sec", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.567403, "span_id": "1"}
{"process": 1217, "levelname": "INFO", "name": "banya", "message": "Redis Cache miss {'bya_vaw_1_60516836_1': (datetime.datetime(2015, 2, 26, 6, 15), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_2_60516836_3': (datetime.datetime(2015, 2, 19, 6, 15), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_2_60516836_2': (datetime.datetime(2015, 2, 19, 6, 15), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_2_60516836_1': (datetime.datetime(2015, 2, 19, 6, 15), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_14_60516836_1': (datetime.datetime(2015, 8, 5, 20, 0), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_14_60516836_3': (datetime.datetime(2015, 8, 5, 20, 0), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_14_60516836_2': (datetime.datetime(2015, 8, 5, 20, 0), datetime.datetime(2015, 4, 2, 5, 15))}, query time 0.040 sec", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086784.944554, "span_id": "1"}
{"process": 1217, "levelname": "INFO", "name": "banya", "message": null, "category": "dependency_start", "context": {"dependency_span_id": "1.2", "args": ["GET", "/ip2geoinfo"], "dependency_name": "geok", "kwargs": {}, "function_name": "_make_request"}, "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086785.12548, "span_id": "1"}
{"process": 1217, "levelname": "INFO", "name": "urllib3.connectionpool", "message": "Starting new HTTP connection (1): geok.els.staging.hulu.com", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086785.127192, "span_id": "1"}
{"process": 1217, "levelname": "STATS", "name": "urllib3.connectionpool", "message": "\"GET /ip2geoinfo?ip=127.0.0.1&no_override=0&preferred_country=US&format=json HTTP/1.1\" 200 35", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086785.190782, "span_id": "1"}
{"process": 1217, "levelname": "INFO", "name": "banya", "message": null, "category": "dependency_end", "context": {"dependency_span_id": "1.2", "dependency_name": "geok", "function_name": "_make_request"}, "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086785.193182, "span_id": "1"}
{"process": 1217, "levelname": "STATS", "name": "banya", "message": "vac - user_id 2000046631, region US, package_group_id 3, asset_id 60516836, device 2, cp_limits [], now_dt 2016-03-04 10:19:44", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086785.194977, "span_id": "1"}
{"process": 1217, "levelname": "ERROR", "name": "banya", "message": "BlockStat: Video not available - user_id 2000046631, cp_limits [], region US, package_group_id 3, asset_id 60516836, device 2, now 2016-03-04 10:19:44", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086785.277804, "span_id": "1", "context": {"block_params": {"asset_id": 60516836, "region": "US", "expires_date": "2015-04-02T05:15", "package_group_id": 3, "available_date": null}, "block_type": "video_expired", "environ": {"SERVER_SOFTWARE": "gevent/1.0 Python/2.7", "SCRIPT_NAME": "", "REQUEST_METHOD": "GET", "PATH_INFO": "/banya_playlist", "SERVER_PROTOCOL": "HTTP/1.1", "QUERY_STRING": "video_id=60516836&token=okNWazHAdddIcV0C2kvRXQ&device=6&version=3&device_id=h99b70153-1b34-7cda-8939-f09603243eb1&x_redirect_header=X-Accel-Redirect&x_redirect=/playlist_end", "REMOTE_ADDR": "127.0.0.1", "HTTP_USER_AGENT": "curl/7.43.0", "SERVER_NAME": "MACBOXYCFH04", "REMOTE_PORT": "49985", "wsgi.url_scheme": "http", "SERVER_PORT": "7986", "werkzeug.request": "<Request 'http://local.hulu.com:7986/banya_playlist?video_id=60516836&token=okNWazHAdddIcV0C2kvRXQ&device=6&version=3&device_id=h99b70153-1b34-7cda-8939-f09603243eb1&x_redirect_header=X-Accel-Redirect&x_redirect=%2Fplaylist_end' [GET]>", "wsgi.input": "<gevent.pywsgi.Input object at 0x1072f2b10>", "HTTP_HOST": "local.hulu.com:7986", "wsgi.multithread": false, "HTTP_ACCEPT": "*/*", "wsgi.version": [1, 0], "GATEWAY_INTERFACE": "CGI/1.1", "wsgi.run_once": false, "wsgi.errors": "<open file '<stderr>', mode 'w' at 0x1047eb1e0>", "wsgi.multiprocess": false, "qs_params": "{'x_redirect_header': ['X-Accel-Redirect'], 'x_redirect': ['/playlist_end'], 'video_id': ['60516836'], 'token': ['okNWazHAdddIcV0C2kvRXQ'], 'version': ['3'], 'device': ['6'], 'device_id': ['h99b70153-1b34-7cda-8939-f09603243eb1']}"}}}
{"process": 1217, "levelname": "STATS", "name": "banya", "message": "video_expired 2130706433 2000046631 2 6", "category": "application", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086785.307173, "span_id": "1"}
{"process": 1217, "levelname": "INFO", "name": "banya", "message": "ending request", "category": "request_end", "service_name": "banya", "human_timestamp": "2016-03-04T02:19", "tracking_id": "9bce2141f85f64e4710090211b6bb39e", "timestamp": 1457086785.312914, "span_id": "1", "context": {}}
''',
        "expected_zipkin_format" : [
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1457086784063047,
                "value": "sr"
            },
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1457086785312913,
                "value": "ss"
            }
        ],
        "binaryAnnotations": [
            {
                "key": "body",
                "value": "{}"
            },
            {
                "key": "header",
                "value": "{u'Host': u'local.hulu.com:7986', u'Accept': u'*/*', u'User-Agent': u'curl/7.43.0'}"
            },
            {
                "key": "param",
                "value": "{u'x_redirect_header': u'X-Accel-Redirect', u'x_redirect': u'/playlist_end', u'video_id': u'60516836', u'token': u'okNWazHAdddIcV0C2kvRXQ', u'version': u'3', u'device': u'6', u'device_id': u'h99b70153-1b34-7cda-8939-f09603243eb1'}"
            },
            {
                "key": "log_event_1",
                "value": "no cached service token, request a new one"
            },
            {
                "key": "log_event_2",
                "value": "send request. endpoint: GetServiceToken, POST https://tut.test.hulu.com:8395/service/token/secret"
            },
            {
                "key": "log_event_3",
                "value": "Starting new HTTPS connection (1): tut.test.hulu.com"
            },
            {
                "key": "log_event_4",
                "value": "\"POST /service/token/secret HTTP/1.1\" 200 274"
            },
            {
                "key": "log_event_5",
                "value": "request service token successfully"
            },
            {
                "key": "log_event_6",
                "value": "send request. endpoint: CheckUserToken, GET https://tut.test.hulu.com:8395/user/check"
            },
            {
                "key": "log_event_7",
                "value": "\"GET /user/check?old_token=True&user_token=okNWazHAdddIcV0C2kvRXQ&hulu_session=False&service_token=lh07WnYChUO_WIqwQ9nmrYIw%2F2E-QlNmF_b96DsKM4ONgS7y7Q--wY9upC50ievKJEP_NZGjQaATKFwpODmCHNtLEWD3BRhyrDxtctabY3eXgB6bNUmQ6otdQN8XBRN18Eb%2FV39_ZQ6lRVZkCFLgirzcB3PZJ2o- HTTP/1.1\" 200 22"
            },
            {
                "key": "log_event_8",
                "value": "request duration: 23"
            },
            {
                "key": "log_event_10",
                "value": "Starting new HTTP connection (1): kardashian.staging.hulu.com"
            },
            {
                "key": "log_event_11",
                "value": "\"GET /user/2000046631 HTTP/1.1\" 200 292"
            },
            {
                "key": "log_event_13",
                "value": "Redis Cache miss bya_vid_60516836_US, query time 0.134 sec"
            },
            {
                "key": "log_event_14",
                "value": "Redis Cache miss {'bya_vaw_1_60516836_1': (datetime.datetime(2015, 2, 26, 6, 15), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_2_60516836_3': (datetime.datetime(2015, 2, 19, 6, 15), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_2_60516836_2': (datetime.datetime(2015, 2, 19, 6, 15), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_2_60516836_1': (datetime.datetime(2015, 2, 19, 6, 15), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_14_60516836_1': (datetime.datetime(2015, 8, 5, 20, 0), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_14_60516836_3': (datetime.datetime(2015, 8, 5, 20, 0), datetime.datetime(2015, 4, 2, 5, 15)), 'bya_vaw_14_60516836_2': (datetime.datetime(2015, 8, 5, 20, 0), datetime.datetime(2015, 4, 2, 5, 15))}, query time 0.040 sec"
            },
            {
                "key": "log_event_16",
                "value": "Starting new HTTP connection (1): geok.els.staging.hulu.com"
            },
            {
                "key": "log_event_17",
                "value": "\"GET /ip2geoinfo?ip=127.0.0.1&no_override=0&preferred_country=US&format=json HTTP/1.1\" 200 35"
            },
            {
                "key": "log_event_19",
                "value": "vac - user_id 2000046631, region US, package_group_id 3, asset_id 60516836, device 2, cp_limits [], now_dt 2016-03-04 10:19:44"
            },
            {
                "key": "log_event_20",
                "value": "BlockStat: Video not available - user_id 2000046631, cp_limits [], region US, package_group_id 3, asset_id 60516836, device 2, now 2016-03-04 10:19:44"
            },
            {
                "key": "log_event_21",
                "value": "video_expired 2130706433 2000046631 2 6"
            }
        ],
        "duration": 1249866,
        "id": "1",
        "name": "banya",
        "timestamp": 1457086784063047,
        "traceId": "9bce2141f85f64e4710090211b6bb39e"
    },
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1457086785125480,
                "value": "cs"
            },
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1457086785193182,
                "value": "cr"
            }
        ],
        "binaryAnnotations": [],
        "duration": 67702,
        "id": "1.2",
        "name": "geok",
        "timestamp": 1457086785125480,
        "traceId": "9bce2141f85f64e4710090211b6bb39e"
    },
    {
        "annotations": [
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1457086784230686,
                "value": "cs"
            },
            {
                "endpoint": {
                    "ipv4": "banya",
                    "port": 0,
                    "serviceName": "banya"
                },
                "timestamp": 1457086784308684,
                "value": "cr"
            }
        ],
        "binaryAnnotations": [],
        "duration": 77998,
        "id": "1.1",
        "name": "kardashian",
        "timestamp": 1457086784230686,
        "traceId": "9bce2141f85f64e4710090211b6bb39e"
    }
],
        "expected_hulu_format" :[
    {
        "label": "banya application call",
        "times": [
            {
                "ending_time": 1457086785312,
                "label": "1249. ms",
                "starting_time": 1457086784063
            }
        ]
    },
    {
        "label": "banya dependency call",
        "times": [
            {
                "ending_time": 1457086784308,
                "label": "kardashian | 77.99 ms",
                "starting_time": 1457086784230
            }
        ]
    },
    {
        "label": "banya dependency call",
        "times": [
            {
                "ending_time": 1457086785193,
                "label": "geok | 67.70 ms",
                "starting_time": 1457086785125
            }
        ]
    }
],

    }
}

if __name__ == "__main__":
    import db
    client = db.get_basic_client()
    for stubname, data in GOOD_STUBS.items():
        tracking_id = data["tracking_id"]
        if "raw_data" not in data:
            print "Generating Data for %s" % stubname
            print client.get_raw(tracking_id)
