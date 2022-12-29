import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

MIN_HEIGHT = 50
MAX_HEIGHT = 500
ROW_HEIGHT = 60


def editable_grid(df):
    # Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(df)

    # customize gridOptions
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True, groupSelectsChildren=False,
                           groupSelectsFiltered=False)
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    # Display the grid
    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        height=300,  # min(MIN_HEIGHT + len(df) * ROW_HEIGHT, MAX_HEIGHT),
        width='100%',
        data_return_mode=DataReturnMode.FILTERED,
        update_mode=GridUpdateMode.GRID_CHANGED,
        fit_columns_on_grid_load=False,
        header_checkbox_selection_filtered_only=True,
        allow_unsafe_jscode=True, theme='alpine',  # Set it to True to allow jsfunction to be injected
    )

    # st.write(type(grid_response['data']))
    st.session_state.og_df.update(grid_response['data']['input'])
    st.session_state.data_updated = True
    if grid_response['selected_rows']:
        selected = grid_response['selected_rows']
        subset = pd.DataFrame.from_dict(selected, orient='columns')
        subset.drop('_selectedRowNodeInfo', axis=1, inplace=True)
        st.write("Selected grid data:")
        st.dataframe(subset)
