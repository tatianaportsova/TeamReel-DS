"""
TeamReel DS API: Fake data to return for front-end dev./testing.
"""

# -------------------------------------------------------------------------
# FAKE INPUT DATA:

FAKE_INPUT_USER_PERFORMANCE = {"user_id": 227}

FAKE_INPUT_PROMPT_TOP_RESPONSES = {"prompt_id": 85}

FAKE_INPUT_VIDEO_ANALYSIS = {"video_id": 156}

# FAKE_INPUT_VIDEO_ANALYZE = to connect to SQS queue polling

# -------------------------------------------------------------------------
# FAKE OUTPUT DATA:

FAKE_OUTPUT_USER_PERFORMANCE = {
    "user_id": 227,
    "video_id": 156,
    "prompt_id": 85,
    "scores": {
        "overall_performance_score": 4.3,
        "human_delivery_and_presentation": 3.4,
        "human_response_quality": 4.7,
        "human_audio_quality": 4.4,
        "human_visual_environment": 3.2,
        "ml_attitude": 4.5,
        "ml_facial_centering": 3.7,
        "ml_speaking_speed": 4.1,
        "ml_background_noise": 3.9
    },
    "scores_progress": {
        "times": [
                  "2020-06-11 16:23:43.657000+0000",
                  "2020-06-11 16:23:43.657000+0000",
                  "2020-06-11 16:23:43.657000+0000",
                  "2020-06-11 16:23:43.657000+0000"
        ],
        "overall_performance": [
                  2.3,
                  3.5,
                  4.0,
                  4.3
        ]
    },
    "charts": {
        "overall_score_progress_chart": {
            "data": [
                      {
                        "uid": "45c0a4",
                        "line": {
                            "color": "rgb(255, 127, 14)",
                            "shape": "spline",
                            "width": 3
                        },
                        "mode": "lines",
                        "name": "iOS & Android",
                        "type": "scatter",
                        "x": [
                            "2007-12-01",
                            "2008-12-01",
                            "2009-12-01",
                            "2010-12-01",
                            "2011-12-01",
                            "2012-12-01",
                            "2013-12-01",
                            "2014-12-01",
                            "2015-12-01"
                        ],
                        "y": [
                            "0",
                            "45560506.663365364",
                            "91145081.21192169",
                            "232447635.15836716",
                            "580348915.5698586",
                            "1182888421.2842617",
                            "1928559640.2194986",
                            "2578825762.2643065",
                            "3022276546.8773637"
                        ]
                    },
                    {
                        "uid": "fc8c63",
                        "line": {
                            "color": "rgb(102, 102, 102)",
                            "shape": "spline",
                            "width": 3
                        },
                        "mode": "lines",
                        "name": "PCs",
                        "type": "scatter",
                        "x": [
                            "2007-12-01",
                            "2008-12-01",
                            "2009-12-01",
                            "2010-12-01",
                            "2011-12-01",
                            "2012-12-01",
                            "2013-12-01",
                            "2014-12-01",
                            "2015-12-01"
                        ],
                        "y": [
                            "970368995.0626459",
                            "1095570133.817442",
                            "1236607941.026805",
                            "1346092750.7529802",
                            "1471269821.6225882",
                            "1517022871.3674688",
                            "1546770777.4614573",
                            "1512907263.0000963",
                            "1463183012.1989794"
                        ]
                    }
            ],
            "layout": {
                "title": " ",
                "width": 1000,
                "xaxis": {
                    "type": "date",
                    "range": [
                        1193687871762.1562,
                        1448946000000
                    ],
                    "title": " ",
                    "showgrid": False,
                    "autorange": True,
                    "tickformat": ""
                },
                "yaxis": {
                    "type": "linear",
                    "range": [
                        -100000000,
                        3600000000
                    ],
                    "title": " ",
                    "autorange": False,
                    "gridcolor": "rgb(208, 208, 208)",
                    "ticksuffix": "  "
                },
                "height": 350,
                "legend": {
                    "x": -0.24796901053454015,
                    "y": 0.9713068181818182,
                    "bgcolor": "rgba(242, 242, 242, 0)",
                    "traceorder": "reversed"
                },
                "margin": {
                    "b": 20,
                    "l": 175,
                    "r": 80,
                    "t": 20
                },
                "autosize": False,
                "annotations": [
                    {
                        "ax": -246,
                        "ay": -164,
                        "font": {
                            "size": 14,
                            "color": "rgb(129, 129, 126)"
                        },
                        "text": "<b>Estimated global install base (bn)</b>",
                        "arrowcolor": "rgba(68, 68, 68, 0)"
                    }
                ],
                "plot_bgcolor": "rgb(242, 242, 242)",
                "paper_bgcolor": "rgb(242, 242, 242)"
            },
            "frames": []
        },
        "overall_score_breakdown_chart": {
            "data": [
                      {
                        "r": [
                          77.5,
                          72.5,
                          70,
                          45,
                          22.5,
                          42.5,
                          40,
                          62.5
                        ],
                        "t": [
                          "North",
                          "N-E",
                          "East",
                          "S-E",
                          "South",
                          "S-W",
                          "West",
                          "N-W"
                        ],
                        "name": "11-14 m/s",
                        "marker": {
                          "color": "rgb(106,81,163)"
                        },
                        "type": "area"
                      },
                      {
                        "r": [
                          57.5,
                          50,
                          45,
                          35,
                          20,
                          22.5,
                          37.5,
                          55
                        ],
                        "t": [
                          "North",
                          "N-E",
                          "East",
                          "S-E",
                          "South",
                          "S-W",
                          "West",
                          "N-W"
                        ],
                        "name": "8-11 m/s",
                        "marker": {
                          "color": "rgb(158,154,200)"
                        },
                        "type": "area"
                      },
                      {
                        "r": [
                          40,
                          30,
                          30,
                          35,
                          7.5,
                          7.5,
                          32.5,
                          40
                        ],
                        "t": [
                          "North",
                          "N-E",
                          "East",
                          "S-E",
                          "South",
                          "S-W",
                          "West",
                          "N-W"
                        ],
                        "name": "5-8 m/s",
                        "marker": {
                          "color": "rgb(203,201,226)"
                        },
                        "type": "area"
                      },
                      {
                        "r": [
                          20,
                          7.5,
                          15,
                          22.5,
                          2.5,
                          2.5,
                          12.5,
                          22.5
                        ],
                        "t": [
                          "North",
                          "N-E",
                          "East",
                          "S-E",
                          "South",
                          "S-W",
                          "West",
                          "N-W"
                        ],
                        "name": "< 5 m/s",
                        "marker": {
                          "color": "rgb(242,240,247)"
                        },
                        "font": {
                          "family": "Arial, sans-serif",
                          "size": 16
                        },
                        "type": "area"
                      }
            ],
            "layout": {
                "title": {"text": "Wind Speed Distribution in Laurel, NE"},
                "font": {
                  "family": "Arial, sans-serif",
                  "size": 16
                },
                "showlegend": False,
                "radialaxis": {
                  "ticksuffix": "%"
                },
                "orientation": 270
            }
        }
    }
}

FAKE_OUTPUT_PROMPT_TOP_RESPONSES = {
    "prompt_id": 85,
    "video_responses_top_3": [
        {
            "user_id": 227,
            "video_id": 156,
            "video_s3_key": "videos/ALPACAVID-Q8H6aTJWG.mp4",
            "video_s3_filename": "ALPACAVID-Q8H6aTJWG.mp4",
            "score_overall_performance": 4.3
        },
        {
            "user_id": 227,
            "video_id": 156,
            "video_s3_key": "videos/ALPACAVID-Q8H6aTJWG.mp4",
            "video_s3_filename": "ALPACAVID-Q8H6aTJWG.mp4",
            "score_overall_performance": 4.3
        },
        {
            "user_id": 227,
            "video_id": 156,
            "video_s3_key": "videos/ALPACAVID-Q8H6aTJWG.mp4",
            "video_s3_filename": "ALPACAVID-Q8H6aTJWG.mp4",
            "score_overall_performance": 4.3
        }
    ]
}

FAKE_OUTPUT_VIDEO_ANALYSIS = {
    "video_id": 156,
    "prompt_id": 85,
    "user_id": 227,
    "scores": {
        "overall_performance_score": 4.3,
        "human_delivery_and_presentation": 3.4,
        "human_response_quality": 4.7,
        "human_audio_quality": 4.4,
        "human_visual_environment": 3.2,
        "ml_attitude": 4.5,
        "ml_facial_centering": 3.7,
        "ml_speaking_speed": 4.1,
        "ml_background_noise": 3.9
    }
}

FAKE_OUTPUT_VIDEO_ANALYZE = "True"
