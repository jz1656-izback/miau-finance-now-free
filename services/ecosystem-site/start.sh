#!/bin/bash
export PATH="/home/jevgeniz/Projekte/miau-finance/ecosystem-site/node_modules/.bin:$PATH"
cd /home/jevgeniz/Projekte/miau-finance/ecosystem-site
serve dist -p 5175 --no-clipboard --single
