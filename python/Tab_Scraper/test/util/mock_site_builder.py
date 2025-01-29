# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:55:01 2025

@author: Sean
"""

import os
import json
from urllib.parse import urljoin

EXPLORER_URL = "https://www.ultimate-guitar.com/"
TABS_URL = "https://tabs.ultimate-guitar.com/tab/"
         
def create_mock_site(mock_adapter):
    _build_mock_explorer(mock_adapter)
    _build_mock_tabs(mock_adapter)
    
def _build_mock_explorer(mock_adapter):
    mock_page_data = json.loads(_get_resource_contents("mock_page_data.json"))
    
    _build_mock_page(
        mock_adapter,
        "mock_page.html",
        urljoin(EXPLORER_URL, "explore?type[]=Tabs"), 
        mock_page_data["page_data_1"]
    )
    
    _build_mock_page(
        mock_adapter, 
        "mock_page.html",
        urljoin(EXPLORER_URL, "explore?type[]=Tabs&page=2"),
        mock_page_data["page_data_2"]
    )
    
    # End of mock site pages
    mock_adapter.register_uri(
        "GET", 
        urljoin(EXPLORER_URL, "explore?type[]=Tabs&page=3"), 
        text="Not Found", 
        status_code=404
    )
    
def _build_mock_tabs(mock_adapter):
    mock_song_data = json.loads(_get_resource_contents("mock_song_data.json"))
    
    _build_mock_page(
        mock_adapter, 
        "mock_song.html",
        urljoin(TABS_URL, "band1/song1"), 
        mock_song_data["song_data_1"]
    )
    
    _build_mock_page(
        mock_adapter, 
        "mock_song.html",
        urljoin(TABS_URL, "band1/song2"), 
        mock_song_data["song_data_2"]
    )
    
    _build_mock_page(
        mock_adapter, 
        "mock_song.html",
        urljoin(TABS_URL, "band2/song1"), 
        mock_song_data["song_data_3"]
    )
    
    _build_mock_page(
        mock_adapter, 
        "mock_song.html",
        urljoin(TABS_URL, "band2/song2"), 
        mock_song_data["song_data_4"]
)
    
def _build_mock_page(mock_adapter, template_file, url, data_mapping):
    template = _get_resource_contents(template_file)
    content = template.format_map(data_mapping)
    _register_mock_uri(mock_adapter, url, content)
    
def _get_resource_contents(file_name):
    resources_dir = os.path.join(os.path.dirname(__file__), "../resources")
    file_path = os.path.join(resources_dir, file_name)

    with open(file_path, "r") as file:
        return file.read()
    
def _register_mock_uri(mock_adapter, url, content):
    mock_adapter.register_uri(
        "GET", 
        url, 
        text=content, 
        headers={"Content-Type": "text/html; charset=utf-8"}
    )