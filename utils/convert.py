import pandas as pd
import xarray as xr


def monthly_csv_to_DataArray(df, freq="MS"):
    """Convert dataframes from NOAA catalog items to xr.DataArray.

    Example:
        >>> cat = intake.open_catalog('master.yaml')
        >>> df = cat.climate.NOAA_correlation.read()
        >>> da = monthly_csv_to_DataArray(df)
        >>> da
        <xr.DataArray> ...
    """
    df = df.set_index("year")
    df = df.apply(pd.to_numeric, errors="coerce")
    initial = df.first_valid_index()
    if len(str(initial)) >= 4:
        initial = str(initial)[:4]
    initial = int(initial)
    return xr.DataArray(
        df.values.flatten(),
        dims="time",
        coords={
            "time": xr.cftime_range(str(initial), freq=freq, periods=df.values.size)
        },
    )
