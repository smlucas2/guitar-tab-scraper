# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:55:01 2025

@author: Sean
"""
         
def create_mock_site(mock_adapter):
    _build_mock_page(mock_adapter, "https://www.ultimate-guitar.com/explore?type[]=Tabs", ["band1", "song1"], ["band1", "song2"])
    _build_mock_page(mock_adapter, "https://www.ultimate-guitar.com/explore?type[]=Tabs&page=2", ["band2", "song1"], ["band2", "song2"])
    # End of mock site pages
    mock_adapter.register_uri("GET", "https://www.ultimate-guitar.com/explore?type[]=Tabs&page=3", text="Not Found", status_code=404)
    
    tab_data_1 = ["0001","1001","0001","Best Song Ever","The Besties","Easy","5", "150"]
    view_data_1 = ["[tab]e|------0------|[/tab]","E A D G B E","Em","150000","125000"]
    _build_mock_song(mock_adapter, "https://tabs.ultimate-guitar.com/tab/band1/song1", tab_data_1, view_data_1)
    
    tab_data_2 = ["0002","1002","0001","Worst Song Ever","The Besties","Easy","1", "60"]
    view_data_2 = ["[tab]e|------2------|[/tab]","E A D G B E","Em","100000","4"]
    _build_mock_song(mock_adapter, "https://tabs.ultimate-guitar.com/tab/band1/song2", tab_data_2, view_data_2)
    
    tab_data_3 = ["0003","1001","0002","Who Cares","Punks","Hard","4", "7000"]
    view_data_3 = ["[tab]e|---1--0----7-|[/tab]","E A D G B E","Em","2000","1000"]
    _build_mock_song(mock_adapter, "https://tabs.ultimate-guitar.com/tab/band2/song1", tab_data_3, view_data_3)
    
    tab_data_4 = ["0004","1002","0002","I Do","Punks","Hard","3", "14000"]
    view_data_4 = ["[tab]e|---4--0--44--|[/tab]","E A D G B E","Em","10000","8000"]
    _build_mock_song(mock_adapter, "https://tabs.ultimate-guitar.com/tab/band2/song2", tab_data_4, view_data_4)
    
def _build_mock_page(mock_adapter, page_url, song_url_components_1, song_url_components_2):
    mock_adapter.register_uri("GET", page_url, text=f"""
        <html>
        <body>
            <div class="js-store" data-content='{{ 
                "store": {{
                    "page": {{
                        "data": {{
                            "data": {{
                                "tabs": [
                                    {{
                                        "tab_url": "https://tabs.ultimate-guitar.com/tab/{song_url_components_1[0]}/{song_url_components_1[1]}"
                                    }},
                                    {{
                                        "tab_url": "https://tabs.ultimate-guitar.com/tab/{song_url_components_2[0]}/{song_url_components_2[1]}"
                                    }}
                                ] 
                            }}
                        }}
                    }}    
                }}
            }}'></div>
        </body>
        </html>
    """, headers={"Content-Type": "text/html; charset=utf-8"})
    
def _build_mock_song(mock_adapter, song_url, tab_data, view_data):
    mock_adapter.register_uri("GET", song_url, text=f"""
        <html>
        <body>
            <div class="js-store" data-content='{{
                "store":{{
                    "page":{{
                        "data":{{
                            "tab":{{
                                "id":"{tab_data[0]}",
                                "song_id":"{tab_data[1]}",
                                "artist_id":"{tab_data[2]}",
                                "song_name":"{tab_data[3]}",
                                "artist_name":"{tab_data[4]}",
                                "difficulty":"{tab_data[5]}",
                                "rating":"{tab_data[6]}",
                                "votes":"{tab_data[7]}"
                            }},
                            "tab_view":{{
                                "wiki_tab":{{
                                    "content":"{view_data[0]}"
                                }},
                                "meta":{{
                                    "tuning":{{
                                        "value":"{view_data[1]}"    
                                    }},
                                    "tonality":"{view_data[2]}"
                                }},
                                "stats":{{
                                    "view_total":"{view_data[3]}",
                                    "favorites_count":"{view_data[4]}"
                                }}
                            }}
                        }}
                    }}  
                }}
            }}'></div>
        </body>
        </html>
    """, headers={"Content-Type": "text/html; charset=utf-8"})