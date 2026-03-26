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
                    if pd.isna(x):
                        return 0
                    str_x = str(x).strip()
                    if str_x.upper().startswith('ORD '):
                        return str_x
                    if str_x.lower() in ['nan', 'none', '', 'null']:
                        return 0
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
    # AI HELPER METHODS
    # ==========================================
    
    @staticmethod
    def _get_ai_response(prompt, session_prefix="ai"):
        """Helper method to get AI response synchronously."""
        if not AI_AVAILABLE:
            return ""
        
        api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not api_key:
            return ""
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            chat = LlmChat(
                api_key=api_key,
                session_id=f"{session_prefix}-{id(prompt)}",
                system_message="You are a data cleaning assistant. Be very concise (1-2 sentences max)."
            ).with_model("gemini", "gemini-2.5-flash")
            
            async def get_response():
                return await chat.send_message(UserMessage(text=prompt))
            
            response = loop.run_until_complete(get_response())
            loop.close()
            return response[:200] if response else ""
        except Exception as e:
            return ""
    
    # ==========================================
    # AI-POWERED CLEANING METHODS
    # ==========================================
    
    @staticmethod
    def clean_missing_values(df, strategy='ai', fill_value=None):
        """
        AI-enhanced handling of missing values for Numeric columns.
        Strategies: 'ai', 'mean', 'median', 'mode', 'constant', 'drop'
        """
        df_clean = df.copy()
        
        # Exclude order-like columns from numeric imputation
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        exclude_cols = ['order', 'id', 'order_id', 'order_number']
        numeric_cols = [col for col in numeric_cols if col.lower() not in exclude_cols]
        
        message = ""

        if strategy == 'drop_rows':
            initial_rows = len(df_clean)
            df_clean = df_clean.dropna()
            message = f"Dropped {initial_rows - len(df_clean)} rows containing missing values."
            df_clean = AIEngine.apply_custom_rules(df_clean)
            return df_clean, message

        if len(numeric_cols) > 0:
            # Get AI analysis
            missing_info = {col: int(df_clean[col].isnull().sum()) for col in numeric_cols if df_clean[col].isnull().any()}
            ai_msg = ""
            if missing_info:
                prompt = f"Briefly analyze missing numeric data and suggest best approach: {missing_info}"
                ai_msg = AIEngine._get_ai_response(prompt, "missing")
            
            if strategy == 'ai':
                # Apply MICE imputation
                cols_with_missing = [col for col in numeric_cols if df_clean[col].isnull().any()]
                if cols_with_missing:
                    imputer = IterativeImputer(random_state=42)
                    df_clean[cols_with_missing] = imputer.fit_transform(df_clean[cols_with_missing])
                message = f"AI Analysis: Applied MICE Algorithm for intelligent imputation. {ai_msg}"
                
            elif strategy == 'mean':
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
                message = f"AI Analysis: Filled with Column Means. {ai_msg}"
                
            elif strategy == 'median':
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
                message = f"AI Analysis: Filled with Column Medians. {ai_msg}"
            
            elif strategy == 'mode':
                for col in numeric_cols:
                    mode_val = df_clean[col].mode()
                    if not mode_val.empty:
                        df_clean[col] = df_clean[col].fillna(mode_val[0])
                message = f"AI Analysis: Filled with Mode values. {ai_msg}"

            elif strategy == 'constant':
                val = fill_value if fill_value is not None else 0
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(val)
                message = f"AI Analysis: Filled with constant value {val}. {ai_msg}"
        else:
            message = "No numeric columns found to clean."
        
        df_clean = AIEngine.apply_custom_rules(df_clean)
        return df_clean, message

    @staticmethod
    def remove_outliers(df):
        """
        AI-enhanced outlier removal using IQR method for Numeric columns.
        """
        df_clean = df.copy()
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        initial_rows = len(df_clean)
        
        outlier_details = []
        for col in numeric_cols:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers_count = len(df_clean[(df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)])
            if outliers_count > 0:
                outlier_details.append(f"{col}: {outliers_count}")
            
            df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
            
        rows_removed = initial_rows - len(df_clean)
        
        # Get AI analysis
        ai_msg = ""
        if outlier_details:
            prompt = f"Briefly comment on outliers removed: {outlier_details}, total {rows_removed} rows removed"
            ai_msg = AIEngine._get_ai_response(prompt, "outlier")
        
        df_clean = AIEngine.apply_custom_rules(df_clean)
        
        details = f" ({', '.join(outlier_details)})" if outlier_details else ""
        message = f"AI Analysis: Removed {rows_removed} outliers using IQR method{details}. {ai_msg}"
        return df_clean, message

    @staticmethod
    def clean_categorical_data(df, strategy='unknown'):
        """
        AI-enhanced handling of missing values for Text/Categorical columns.
        """
        df_clean = df.copy()
        cat_cols = df_clean.select_dtypes(include=['object']).columns
        
        if len(cat_cols) == 0:
            df_clean = AIEngine.apply_custom_rules(df_clean)
            return df_clean, "No text columns found to clean."

        filled_count = 0
        cleaned_cols = []
        
        for col in cat_cols:
            missing_count = df_clean[col].isnull().sum()
            if missing_count > 0:
                if strategy == 'mode':
                    mode_val = df_clean[col].mode()
                    if not mode_val.empty:
                        df_clean[col] = df_clean[col].fillna(mode_val[0])
                        filled_count += 1
                        cleaned_cols.append(f"{col}: {missing_count}")
                else:
                    df_clean[col] = df_clean[col].fillna('Unknown')
                    filled_count += 1
                    cleaned_cols.append(f"{col}: {missing_count}")
        
        # Get AI analysis
        ai_msg = ""
        if cleaned_cols:
            samples = {col: df[col].dropna().unique()[:3].tolist() for col in list(cat_cols)[:3]}
            prompt = f"Briefly analyze text cleaning: filled {cleaned_cols}, sample values: {samples}"
            ai_msg = AIEngine._get_ai_response(prompt, "text")
        
        df_clean = AIEngine.apply_custom_rules(df_clean)
        
        details = f" ({', '.join(cleaned_cols)})" if cleaned_cols else ""
        msg = f"AI Analysis: Cleaned {filled_count} text columns{details}. {ai_msg}"
        return df_clean, msg
    
    @staticmethod
    def remove_duplicates(df):
        """AI-enhanced duplicate removal from the dataframe."""
        df_clean = df.copy()
        initial_rows = len(df_clean)
        
        duplicate_count = df_clean.duplicated().sum()
        df_clean = df_clean.drop_duplicates()
        rows_removed = initial_rows - len(df_clean)
        
        # Get AI analysis
        ai_msg = ""
        if duplicate_count > 0:
            prompt = f"Briefly comment on removing {duplicate_count} duplicates from {initial_rows} rows"
            ai_msg = AIEngine._get_ai_response(prompt, "dup")
        
        df_clean = AIEngine.apply_custom_rules(df_clean)
        
        message = f"AI Analysis: Removed {rows_removed} duplicate rows. {ai_msg}"
        return df_clean, message
