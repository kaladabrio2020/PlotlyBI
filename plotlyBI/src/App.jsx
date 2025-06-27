import React from "react";

import { Button, Dropdown, Space, Select } from 'antd';
import { FileOutlined } from '@ant-design/icons';

// icons
import postgresIcon   from "./assets/icons/postgres.png";
import duckdbIcon     from "./assets/icons/duckdb.png";
import mysqlIcon      from "./assets/icons/mysql.png";
import bigqueryIcon   from "./assets/icons/google.png";


// Styles 
import "./styles/App.css";


// Components

const colourOptions = [
    { value: 'ocean', label: 'Ocean', color: '#00B8D9' },
    { value: 'blue', label: 'Blue', color: '#0052CC' },
    { value: 'purple', label: 'Purple', color: '#5243AA' },
    { value: 'red', label: 'Red', color: '#FF5630' },
];
const menuItems = [
  { key: "1", label: "Import csv file", icon: <FileOutlined /> },
  { 
    key: "2", 
    label:(
        <Space>
            <img src={postgresIcon} alt="Postgres" style={{ width: 13, height: 13 }} />
            Postgres 
        </Space>
    )
  },
  { 
    key: "3", 
    label: (
        <Space>
            <img src={mysqlIcon} alt="MySQL" style={{ width: 13, height: 13 }} />
            MySQL
        </Space>
    )
 },
  { 
    key: "4", 
    label: (
        <Space>
            <img src={duckdbIcon} alt="DuckDB" style={{ width: 13, height: 13 }} />
            DuckDB
        </Space>
    ) 

  },
  { 
    key: "5", 
    label: (
        <Space>
            <img src={bigqueryIcon} alt="BigQuery" style={{ width: 12, height: 12 }} />
            BigQuery
        </Space>
    ) 
  },
];

export default function App() {
    return (
        <>
        <div>
            <div className="bar-top-home">

                <div className="div-connection-select">
                    <div className="div-connection">
                        <Space wrap>
                            <Dropdown menu={{ items: menuItems }} placement="bottom" arrow trigger={['click']}> 
                                <Button type="primary">
                                    Connection
                                </Button>
                            </Dropdown>
                        </Space>
                    </div>
                    <div>
                        <Space>
                            <Select
                                style={{ width: 250 }}
                                options={colourOptions}
                                placeholder="Select a table"
                                allowClear
                            />
                        </Space>
                    </div>
                </div>

                <div className="div-metrics-dimensions">
                    <div className="div-dimensions">
                        <p>Dimensions</p>
        
                        <p>Metrics</p>
                    </div>
                    <div className="div-multiple-select-metrics-dimensions">
                        <div>
                            
                        <Select
                            mode="multiple"
                            options={colourOptions}
                            style={{ width: 700 , marginTop: 10, marginBottom: 5, height:30}}
                            allowClear
                        />
                        </div>
                        <div>

                        <Select
                            mode="multiple"
                            options={colourOptions}
                            style={{ width: 700 ,height:30}}
                            allowClear
                        />
                        </div>

                    </div>
                </div>

            </div>
        </div>
        </>
    );
}