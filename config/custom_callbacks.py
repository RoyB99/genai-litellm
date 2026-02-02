from litellm.integrations.custom_logger import CustomLogger
import litellm

class DropAnthropicParams(CustomLogger):
    """
    Custom callback to drop Anthropic-specific parameters
    that are not supported by Azure OpenAI.
    """
    
    params_to_drop = [
        'context_management',
        'prompt_caching', 
        'betas',
        'metadata',
        'stop_sequences',
        'top_k',
    ]
    
    async def async_pre_call_hook(self, user_api_key_dict, cache, data, call_type):
        """Called before the LLM API call - this runs before validation"""
        for param in self.params_to_drop:
            data.pop(param, None)
        return data
    
    def log_pre_api_call(self, model, messages, kwargs):
        # Drop from top-level kwargs
        for param in self.params_to_drop:
            kwargs.pop(param, None)
        
        # Drop from optional_params if present
        if 'optional_params' in kwargs:
            for param in self.params_to_drop:
                kwargs['optional_params'].pop(param, None)
        
        # Drop from litellm_params if present
        if 'litellm_params' in kwargs:
            for param in self.params_to_drop:
                kwargs['litellm_params'].pop(param, None)

drop_handler = DropAnthropicParams()
