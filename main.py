import dash
from dash import dcc, html, Input, Output, State, callback_context
from dash.dependencies import MATCH, ALL
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

# Dados de exemplo (você pode substituir por seus dados reais)
def criar_dados_exemplo():
    import numpy as np
    np.random.seed(42)
    
    data = {
        'Vendas': np.random.randint(1000, 10000, 100),
        'Lucro': np.random.randint(100, 2000, 100),
        'Quantidade': np.random.randint(10, 100, 100),
        'Desconto': np.random.uniform(0, 0.3, 100),
        'Categoria': np.random.choice(['Eletrônicos', 'Roupas', 'Casa', 'Esportes'], 100),
        'Região': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], 100),
        'Mês': np.random.choice(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'], 100),
        'Ano': np.random.choice([2022, 2023, 2024], 100)
    }
    return pd.DataFrame(data)

df = criar_dados_exemplo()

# Inicializar app
app = dash.Dash(__name__)

# CSS para redimensionamento
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
        .resizable-chart {
            position: relative;
            border: 2px solid #ddd;
            border-radius: 10px;
            margin-bottom: 20px;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            resize: both;
            overflow: hidden;
            min-width: 300px;
            min-height: 200px;
        }
        
        .resizable-chart:hover {
            border-color: #3498db;
        }
        
        .chart-header {
            background: #f8f9fa;
            padding: 10px 15px;
            border-bottom: 1px solid #ddd;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: move;
        }
        
        .chart-content {
            height: calc(100% - 50px);
            overflow: hidden;
        }
        
        .chart-controls {
            display: flex;
            gap: 5px;
        }
        
        .control-btn {
            background: none;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 2px 6px;
            cursor: pointer;
            font-size: 12px;
        }
        
        .control-btn:hover {
            background: #f0f0f0;
        }
        
        .size-presets {
            display: flex;
            gap: 5px;
            margin: 5px 0;
        }
        
        .size-btn {
            background: #3498db;
            color: white;
            border: none;
            padding: 2px 8px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 10px;
        }
        
        .size-btn:hover {
            background: #2980b9;
        }
        
        .draggable {
            position: absolute;
            z-index: 1000;
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
    <script>
        // Função para tornar elementos arrastáveis
        function makeDraggable(element) {
            let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
            const header = element.querySelector('.chart-header');
            
            if (header) {
                header.onmousedown = dragMouseDown;
            }
            
            function dragMouseDown(e) {
                e = e || window.event;
                e.preventDefault();
                pos3 = e.clientX;
                pos4 = e.clientY;
                document.onmouseup = closeDragElement;
                document.onmousemove = elementDrag;
                element.style.position = 'absolute';
                element.style.zIndex = '1000';
            }
            
            function elementDrag(e) {
                e = e || window.event;
                e.preventDefault();
                pos1 = pos3 - e.clientX;
                pos2 = pos4 - e.clientY;
                pos3 = e.clientX;
                pos4 = e.clientY;
                element.style.top = (element.offsetTop - pos2) + "px";
                element.style.left = (element.offsetLeft - pos1) + "px";
            }
            
            function closeDragElement() {
                document.onmouseup = null;
                document.onmousemove = null;
            }
        }
        
        // Observar mudanças no DOM para aplicar funcionalidades
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && node.classList.contains('resizable-chart')) {
                        makeDraggable(node);
                    }
                });
            });
        });
        
        observer.observe(document.body, { childList: true, subtree: true });
    </script>
</body>
</html>
'''

# Estilos CSS
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("📊 Dashboard Interativo", style={'color': 'white', 'margin': '0', 'textAlign': 'center'})
    ], style={'backgroundColor': '#2c3e50', 'padding': '20px', 'marginBottom': '20px'}),
    
    # Painel de controles
    html.Div([
        html.Div([
            html.H3("🔧 Controles", style={'color': '#2c3e50', 'marginBottom': '20px'}),
            
            # Seleção de colunas
            html.Div([
                html.Label("Eixo X:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='dropdown-x',
                    options=[{'label': col, 'value': col} for col in df.columns],
                    value='Categoria',
                    style={'marginBottom': '15px'}
                )
            ]),
            
            html.Div([
                html.Label("Eixo Y:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='dropdown-y',
                    options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['number']).columns],
                    value='Vendas',
                    style={'marginBottom': '15px'}
                )
            ]),
            
            html.Div([
                html.Label("Cor/Agrupamento (opcional):", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='dropdown-color',
                    options=[{'label': 'Nenhum', 'value': None}] + 
                            [{'label': col, 'value': col} for col in df.select_dtypes(include=['object']).columns],
                    value=None,
                    style={'marginBottom': '15px'}
                )
            ]),
            
            # Tipo de gráfico
            html.Div([
                html.Label("Tipo de Gráfico:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='dropdown-chart-type',
                    options=[
                        {'label': '📊 Barras', 'value': 'bar'},
                        {'label': '📈 Linha', 'value': 'line'},
                        {'label': '🔵 Dispersão', 'value': 'scatter'},
                        {'label': '🥧 Pizza', 'value': 'pie'},
                        {'label': '📦 Box Plot', 'value': 'box'},
                        {'label': '📊 Histograma', 'value': 'histogram'},
                        {'label': '🗺️ Mapa de Calor', 'value': 'heatmap'}
                    ],
                    value='bar',
                    style={'marginBottom': '15px'}
                )
            ]),
            
            # Agregação
            html.Div([
                html.Label("Agregação:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='dropdown-agg',
                    options=[
                        {'label': 'Soma', 'value': 'sum'},
                        {'label': 'Média', 'value': 'mean'},
                        {'label': 'Contagem', 'value': 'count'},
                        {'label': 'Máximo', 'value': 'max'},
                        {'label': 'Mínimo', 'value': 'min'}
                    ],
                    value='sum',
                    style={'marginBottom': '15px'}
                )
            ]),
            
            # Botão para adicionar gráfico
            html.Button(
                "➕ Adicionar Gráfico",
                id='btn-add-chart',
                n_clicks=0,
                style={
                    'backgroundColor': '#3498db',
                    'color': 'white',
                    'border': 'none',
                    'padding': '10px 20px',
                    'borderRadius': '5px',
                    'cursor': 'pointer',
                    'fontSize': '16px',
                    'width': '100%'
                }
            )
            
        ], style={
            'backgroundColor': '#ecf0f1',
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        })
        
    ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),
    
    # Área dos gráficos
    html.Div([
        html.Div(id='charts-container', children=[
            html.H3("👆 Use os controles à esquerda para criar gráficos", 
                   style={'textAlign': 'center', 'color': '#7f8c8d', 'marginTop': '100px'})
        ])
    ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '0 10px'}),
    
    # Store para armazenar gráficos
    dcc.Store(id='charts-store', data=[]),
    
    # Store para armazenar tamanhos dos gráficos
    dcc.Store(id='chart-sizes-store', data={})
    
], style={'fontFamily': 'Arial, sans-serif', 'margin': '0', 'padding': '0'})

# Callback para adicionar gráficos
@app.callback(
    [Output('charts-store', 'data'),
     Output('charts-container', 'children')],
    [Input('btn-add-chart', 'n_clicks')],
    [State('dropdown-x', 'value'),
     State('dropdown-y', 'value'),
     State('dropdown-color', 'value'),
     State('dropdown-chart-type', 'value'),
     State('dropdown-agg', 'value'),
     State('charts-store', 'data')]
)
def add_chart(n_clicks, x_col, y_col, color_col, chart_type, agg_func, current_charts):
    if n_clicks == 0:
        return current_charts, [html.H3("👆 Use os controles à esquerda para criar gráficos", 
                                       style={'textAlign': 'center', 'color': '#7f8c8d', 'marginTop': '100px'})]
    
    # Criar configuração do gráfico
    chart_config = {
        'id': f'chart-{len(current_charts)}',
        'x': x_col,
        'y': y_col,
        'color': color_col,
        'type': chart_type,
        'agg': agg_func,
        'title': f'{chart_type.title()} - {y_col} por {x_col}'
    }
    
    # Adicionar à lista
    updated_charts = current_charts + [chart_config]
    
    # Criar os componentes visuais
    chart_components = []
    for i, config in enumerate(updated_charts):
        fig = create_figure(config)
        
        # Tamanho padrão ou salvo
        default_size = {'width': '100%', 'height': '400px'}
        
        chart_div = html.Div([
            # Header com controles
            html.Div([
                html.Div([
                    html.H4(config['title'], style={'margin': '0', 'color': '#2c3e50', 'fontSize': '14px'}),
                    html.Div([
                        html.Button("📏", id={'type': 'btn-resize', 'index': i}, className='control-btn', title='Redimensionar'),
                        html.Button("📌", id={'type': 'btn-pin', 'index': i}, className='control-btn', title='Fixar posição'),
                        html.Button("🔄", id={'type': 'btn-refresh', 'index': i}, className='control-btn', title='Atualizar'),
                        html.Button("❌", id={'type': 'btn-remove', 'index': i}, className='control-btn', title='Remover',
                                  style={'color': '#e74c3c', 'fontWeight': 'bold'})
                    ], className='chart-controls')
                ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}),
                
                # Presets de tamanho
                html.Div([
                    html.Button("P", id={'type': 'size-small', 'index': i}, className='size-btn', title='Pequeno'),
                    html.Button("M", id={'type': 'size-medium', 'index': i}, className='size-btn', title='Médio'),
                    html.Button("G", id={'type': 'size-large', 'index': i}, className='size-btn', title='Grande'),
                    html.Button("XL", id={'type': 'size-xlarge', 'index': i}, className='size-btn', title='Extra Grande'),
                ], className='size-presets')
                
            ], className='chart-header'),
            
            # Conteúdo do gráfico
            html.Div([
                dcc.Graph(
                    figure=fig, 
                    style={'height': '100%', 'width': '100%'},
                    config={'displayModeBar': True, 'displaylogo': False}
                )
            ], className='chart-content')
            
        ], 
        className='resizable-chart',
        id={'type': 'chart-container', 'index': i},
        style={
            'width': '100%',
            'height': '400px',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'margin': '10px'
        })
        
        chart_components.append(chart_div)
    
    return updated_charts, chart_components

# Callback para redimensionar gráficos
@app.callback(
    Output({'type': 'chart-container', 'index': MATCH}, 'style'),
    [Input({'type': 'size-small', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'size-medium', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'size-large', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'size-xlarge', 'index': MATCH}, 'n_clicks')],
    [State({'type': 'chart-container', 'index': MATCH}, 'style')],
    prevent_initial_call=True
)
def resize_chart(small_clicks, medium_clicks, large_clicks, xlarge_clicks, current_style):
    ctx = callback_context
    if not ctx.triggered:
        return current_style
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_type = eval(button_id)['type']
    
    # Definir tamanhos baseados no botão clicado
    sizes = {
        'size-small': {'width': '300px', 'height': '250px'},
        'size-medium': {'width': '450px', 'height': '350px'},
        'size-large': {'width': '600px', 'height': '450px'},
        'size-xlarge': {'width': '800px', 'height': '600px'}
    }
    
    new_style = current_style.copy()
    new_style.update(sizes[button_type])
    new_style.update({
        'display': 'inline-block',
        'verticalAlign': 'top',
        'margin': '10px'
    })
    
    return new_style

def create_figure(config):
    """Criar figura baseada na configuração"""
    x_col = config['x']
    y_col = config['y']
    color_col = config['color']
    chart_type = config['type']
    agg_func = config['agg']
    
    # Preparar dados baseado na agregação
    if chart_type in ['pie']:
        # Para pizza, sempre agregar
        if color_col:
            df_agg = df.groupby([x_col, color_col])[y_col].agg(agg_func).reset_index()
        else:
            df_agg = df.groupby(x_col)[y_col].agg(agg_func).reset_index()
    elif chart_type in ['bar', 'line'] and x_col in df.select_dtypes(include=['object']).columns:
        # Para categóricas, agregar
        if color_col:
            df_agg = df.groupby([x_col, color_col])[y_col].agg(agg_func).reset_index()
        else:
            df_agg = df.groupby(x_col)[y_col].agg(agg_func).reset_index()
    else:
        # Para dados contínuos, usar dados originais
        df_agg = df
    
    # Criar gráfico baseado no tipo
    if chart_type == 'bar':
        fig = px.bar(df_agg, x=x_col, y=y_col, color=color_col, 
                     title=f'{y_col} por {x_col}')
    elif chart_type == 'line':
        fig = px.line(df_agg, x=x_col, y=y_col, color=color_col,
                      title=f'{y_col} por {x_col}')
    elif chart_type == 'scatter':
        fig = px.scatter(df_agg, x=x_col, y=y_col, color=color_col,
                         title=f'{y_col} vs {x_col}')
    elif chart_type == 'pie':
        fig = px.pie(df_agg, names=x_col, values=y_col,
                     title=f'Distribuição de {y_col} por {x_col}')
    elif chart_type == 'box':
        fig = px.box(df, x=x_col, y=y_col, color=color_col,
                     title=f'Box Plot - {y_col} por {x_col}')
    elif chart_type == 'histogram':
        fig = px.histogram(df, x=y_col, color=color_col,
                          title=f'Histograma - {y_col}')
    elif chart_type == 'heatmap':
        # Criar matriz de correlação ou pivot table
        if color_col:
            pivot_df = df.pivot_table(values=y_col, index=x_col, columns=color_col, aggfunc=agg_func, fill_value=0)
            fig = px.imshow(pivot_df, title=f'Mapa de Calor - {y_col}', aspect='auto')
        else:
            corr_df = df.select_dtypes(include=['number']).corr()
            fig = px.imshow(corr_df, title='Mapa de Calor - Correlação', aspect='auto')
    
    # Personalizar layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#2c3e50'},
        margin={'l': 40, 'r': 40, 't': 60, 'b': 40}
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)