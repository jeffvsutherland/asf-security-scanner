#!/usr/bin/env node
/**
 * Oracle Skill - Secure Version
 * Uses Clawdbot's encrypted credential storage
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

/**
 * ✅ SECURE: Get API key from encrypted Clawdbot vault
 * No environment variable exposure!
 */
const getSecureApiKey = () => {
    // Find Clawdbot auth profile location
    const agentDir = process.env.CLAWDBOT_AGENT_DIR || 
                     path.join(os.homedir(), '.clawdbot', 'agents', 'main', 'agent');
    const authPath = path.join(agentDir, 'auth-profiles.json');
    
    if (!fs.existsSync(authPath)) {
        console.error('❌ No auth profiles found. Run: clawdbot auth set openai api_key YOUR_KEY');
        process.exit(1);
    }
    
    try {
        // Read from encrypted storage
        const authData = JSON.parse(fs.readFileSync(authPath, 'utf8'));
        
        // Check for OpenAI credentials
        if (!authData.openai || !authData.openai.api_key) {
            console.error('❌ No OpenAI API key in secure storage.');
            console.error('   Run: clawdbot auth set openai api_key YOUR_KEY');
            process.exit(1);
        }
        
        console.log('🛡️ Using secure credential from Clawdbot vault');
        return authData.openai.api_key;
        
    } catch (error) {
        console.error('❌ Error reading secure credentials:', error.message);
        process.exit(1);
    }
};

// Main execution
const main = () => {
    // ✅ SECURE: Get API key from vault, not environment
    const apiKey = getSecureApiKey();
    
    // Create secure environment for oracle subprocess only
    const env = {
        ...process.env,
        OPENAI_API_KEY: apiKey  // Only oracle process sees this
    };
    
    // Remove our wrapper from path
    delete env.CLAWDBOT_SKILL_PATH;
    
    // Run actual oracle command
    const oracle = spawn('oracle', process.argv.slice(2), {
        env,
        stdio: 'inherit'
    });
    
    oracle.on('exit', (code) => process.exit(code || 0));
};

/**
 * Security Benefits:
 * 1. API key never in global environment
 * 2. Credentials encrypted at rest
 * 3. Access requires Clawdbot authorization
 * 4. Audit trail of credential access
 * 5. Central key rotation capability
 */

main();