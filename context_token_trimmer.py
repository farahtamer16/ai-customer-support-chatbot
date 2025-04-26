# Estimate tokens based on character count (approx. 1 token = 4 chars)
def estimate_tokens(messages):
    total_chars = sum(len(m['content']) for m in messages)
    return total_chars // 4  # rough estimate

# Trim memory to stay under token limit (e.g. 8192 for DeepSeek)
def trim_memory_to_fit(memory, system_prompt, max_tokens=6000):
    # Prepend system message to memory for estimation
    messages = [{"role": "system", "content": system_prompt}] + memory
    while estimate_tokens(messages) > max_tokens:
        if len(memory) > 1:
            memory.pop(0)  # Remove oldest turn
            messages = [{"role": "system", "content": system_prompt}] + memory
        else:
            break
    return memory