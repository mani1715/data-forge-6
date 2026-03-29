import pandas as pd
import numpy as np
import os
import asyncio
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer

# AI Integration
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class AIEngine:
    
    # ==========================================
    # CUSTOM RULES - STRICT FORMATTING
    # ==========================================
    
    @staticmethod
    def apply_custom_rules(df):
        """
        Apply strict formatting rules to specific fields.
        Called AFTER all cleaning operations.
        """
        df_clean = df.copy()
        
        # 1. DATE FIELD - If missing → "00-00-0000"
        if "date" in df_clean.columns:
            df_clean["date"] = df_clean["date"].fillna("00-00-0000")
            df_clean["date"] = df_clean["date"].astype(str)
            # Replace any 'nan' strings
            df_clean["date"] = df_clean["date"].replace(['nan', 'NaN', 'None', ''], "00-00-0000")
        
        # 2. NAME FIELD - Convert to proper case
        if "name" in df_clean.columns:
            df_clean["name"] = df_clean["name"].astype(str).str.strip()
            df_clean["name"] = df_clean["name"].apply(
                lambda x: x.capitalize() if x and x.lower() not in ['nan', 'none', ''] else "Unknown"
            )
        
        # 3. ORDER FIELD - Format as "ORD X" or 0 if missing
        if "order" in df_clean.columns:
            def format_order(x):
                try:
                    # Check for missing/null values
                    if pd.isna(x):
                        return 0
                    
                    str_x = str(x).strip()
                    
                    # If already formatted as "ORD X", return as-is
                    if str_x.upper().startswith('ORD '):
                        return str_x
                    
                    # Check for null-like strings
                    if str_x.lower() in ['nan', 'none', '', 'null']:
                        return 0
                    
                    # Try to get numeric value
                    val = int(float(x))
                    if val == 0:
                        return 0
                    return f"ORD {val}"
                except (ValueError, TypeError):
                    return 0
            
            df_clean["order"] = df_clean["order"].apply(format_order)
        
        # 4. PRICE FIELD - If missing → 0
        if "price" in df_clean.columns:
            df_clean["price"] = pd.to_numeric(df_clean["price"], errors='coerce').fillna(0)
        
        # 5. PRODUCT NAME - If missing → "Unknown"
        if "product" in df_clean.columns:
            df_clean["product"] = df_clean["product"].fillna("Unknown")
            df_clean["product"] = df_clean["product"].astype(str)
            df_clean["product"] = df_clean["product"].replace(['nan', 'NaN', 'None', ''], "Unknown")
        
        return df_clean
    
    # ==========================================
    # AI-POWERED CLEANING WITH GEMINI
    # ==========================================
    
    @staticmethod
    async def ai_clean_with_gemini(df, columns_to_clean=None):
        """
        Use Gemini AI for intelligent data cleaning suggestions.
        This is a HYBRID system - AI enhances but doesn't replace logic.
        """
        if not AI_AVAILABLE:
            return df, "AI module not available. Using standard cleaning."
        
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            return df, "AI key not configured. Using standard cleaning."
        
        try:
            # Initialize Gemini chat
            chat = LlmChat(
                api_key=api_key,
                session_id=f"dataforge-{id(df)}",
                system_message="You are a data cleaning assistant. Analyze data and suggest fixes. Be concise."
            ).with_model("gemini", "gemini-2.5-flash")
            
            # Prepare data sample for AI analysis
            sample_data = df.head(20).to_dict()
            columns_info = {col: str(df[col].dtype) for col in df.columns}
            missing_info = df.isnull().sum().to_dict()
            
            prompt = f"""Analyze this dataset and provide cleaning recommendations:

Columns and types: {columns_info}
Missing values per column: {missing_info}
Sample data (first 20 rows): {sample_data}

Provide brief recommendations for:
1. Which columns need attention
2. Suggested fill values for missing data
3. Any data format issues detected

Be concise - max 3 sentences per point."""

            user_message = UserMessage(text=prompt)
            response = await chat.send_message(user_message)
            
            return df, f"AI Analysis: {response[:500]}"  # Truncate long responses
            
        except Exception as e:
            return df, f"AI analysis unavailable: {str(e)[:100]}"
    
    @staticmethod
    def ai_clean_data_sync(df):
        """Synchronous wrapper for AI cleaning."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(AIEngine.ai_clean_with_gemini(df))
            loop.close()
            return result
        except Exception as e:
            return df, f"AI cleaning skipped: {str(e)[:100]}"
    
    # ==========================================
    # EXISTING CLEANING METHODS
    # ==========================================
    
    @staticmethod
    def clean_missing_values(df, strategy='ai', fill_value=None):
        """
        Handles missing values for Numeric columns.
        Strategies: 'ai', 'mean', 'median', 'mode', 'constant', 'drop'
        """
        df_clean = df.copy()
        
        # Get numeric columns, but EXCLUDE 'order' column from numeric imputation
        # (order is a categorical/ID field that should not be statistically imputed)
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        exclude_cols = ['order', 'id', 'order_id', 'order_number']
        numeric_cols = [col for col in numeric_cols if col.lower() not in exclude_cols]
        
        message = ""

        if strategy == 'drop_rows':
            initial_rows = len(df_clean)
            df_clean = df_clean.dropna()
            message = f"Dropped {initial_rows - len(df_clean)} rows containing missing values."
            # Apply custom rules after cleaning
            df_clean = AIEngine.apply_custom_rules(df_clean)
            return df_clean, message

        if len(numeric_cols) > 0:
            if strategy == 'ai':
                # Try AI-enhanced cleaning first
                df_clean, ai_msg = AIEngine.ai_clean_data_sync(df_clean)
                
                # Then apply MICE imputation ONLY to numeric columns that need it
                cols_with_missing = [col for col in numeric_cols if df_clean[col].isnull().any()]
                if cols_with_missing:
                    imputer = IterativeImputer(random_state=42)
                    df_clean[cols_with_missing] = imputer.fit_transform(df_clean[cols_with_missing])
                message = f"Applied AI-based Imputation (MICE Algorithm). {ai_msg}"
                
            elif strategy == 'mean':
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
                message = "Filled missing values with Column Means."
                
            elif strategy == 'median':
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
                message = "Filled missing values with Column Medians."
            
            elif strategy == 'mode':
                for col in numeric_cols:
                    mode_val = df_clean[col].mode()
                    if not mode_val.empty:
                        df_clean[col] = df_clean[col].fillna(mode_val[0])
                message = "Filled missing values with Mode."

            elif strategy == 'constant':
                val = fill_value if fill_value is not None else 0
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(val)
                message = f"Filled missing values with constant value: {val}."
        else:
            message = "No numeric columns found to clean."
        
        # Apply custom rules after cleaning
        df_clean = AIEngine.apply_custom_rules(df_clean)
        return df_clean, message

    @staticmethod
    def remove_outliers(df):
        """
        Removes outliers using the IQR method for Numeric columns.
        """
        df_clean = df.copy()
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        initial_rows = len(df_clean)
        
        for col in numeric_cols:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
            
        rows_removed = initial_rows - len(df_clean)
        
        # Apply custom rules after cleaning
        df_clean = AIEngine.apply_custom_rules(df_clean)
        return df_clean, f"Removed {rows_removed} outliers using IQR method."

    @staticmethod
    def clean_categorical_data(df, strategy='unknown'):
        """
        Handles missing values for Text/Categorical columns.
        Strategy: 'unknown' fills with 'Unknown', 'mode' fills with most frequent.
        """
        df_clean = df.copy()
        cat_cols = df_clean.select_dtypes(include=['object']).columns
        
        if len(cat_cols) == 0:
            df_clean = AIEngine.apply_custom_rules(df_clean)
            return df_clean, "No text columns found to clean."

        filled_count = 0
        
        for col in cat_cols:
            if df_clean[col].isnull().sum() > 0:
                if strategy == 'mode':
                    mode_val = df_clean[col].mode()
                    if not mode_val.empty:
                        df_clean[col] = df_clean[col].fillna(mode_val[0])
                        filled_count += 1
                else:
                    # Default: Fill with 'Unknown'
                    df_clean[col] = df_clean[col].fillna('Unknown')
                    filled_count += 1
        
        # Apply custom rules after cleaning
        df_clean = AIEngine.apply_custom_rules(df_clean)
        msg = f"Cleaned {filled_count} text columns using strategy: {strategy}."
        return df_clean, msg
    
    @staticmethod
    def remove_duplicates(df):
        """Remove duplicate rows from the dataframe."""
        df_clean = df.copy()
        initial_rows = len(df_clean)
        df_clean = df_clean.drop_duplicates()
        rows_removed = initial_rows - len(df_clean)
        
        # Apply custom rules after cleaning
        df_clean = AIEngine.apply_custom_rules(df_clean)
        return df_clean, f"Removed {rows_removed} duplicate rows."
