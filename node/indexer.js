const fs = require('fs');
const path = require('path');
const mammoth = require('mammoth');
const pdfParse = require('pdf-parse');

async function extractText(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    try {
        if (ext === '.docx') {
            const result = await mammoth.extractRawText({ path: filePath });
            return result.value;
        } else if (ext === '.pdf') {
            const dataBuffer = fs.readFileSync(filePath);
            const data = await pdfParse(dataBuffer);
            return data.text;
        } else if (['.txt', '.md', '.rtf'].includes(ext)) {
            return fs.readFileSync(filePath, 'utf8');
        } else if (['.xlsx', '.pptx', '.doc', '.ppt', '.xls'].includes(ext)) {
            return `Metadata: ${path.basename(filePath)}`;
        }
    } catch (e) {
        return `Error reading ${filePath}: ${e.message}`;
    }
    return '';
}

async function main() {
    const rootDir = path.resolve(process.argv[2] || '../..');
    const filesToProcess = [];

    function walk(dir) {
        const list = fs.readdirSync(dir);
        list.forEach(file => {
            const fullPath = path.join(dir, file);
            const stat = fs.statSync(fullPath);
            if (stat && stat.isDirectory()) {
                if (!file.startsWith('.') && file !== 'scripts' && file !== 'node_modules') {
                    walk(fullPath);
                }
            } else {
                filesToProcess.push(fullPath);
            }
        });
    }

    walk(rootDir);

    console.log(`Indexando a TOTALIDADE de ${filesToProcess.length} arquivos...`);
    const index = [];
    let count = 0;

    for (const file of filesToProcess) {
        count++;
        if (count % 100 === 0) process.stdout.write(`\rProcessado ${count}/${filesToProcess.length}...`);
        
        try {
            const ext = path.extname(file).toLowerCase();
            let text = "";
            
            // Só faz extração pesada em documentos de texto/pdf
            if (['.pdf', '.docx', '.txt', '.md', '.rtf'].includes(ext)) {
                text = await extractText(file);
            } else {
                text = `Metadata: ${path.basename(file)} ext: ${ext}`;
            }

            if (typeof text !== 'string') text = String(text || '');
            
            index.push({
                path: path.relative(rootDir, file),
                contentSnippet: text.substring(0, 2000).replace(/\s+/g, ' ').trim()
            });
        } catch (err) {
            index.push({
                path: path.relative(rootDir, file),
                contentSnippet: `Error: ${err.message}`
            });
        }
    }

    console.log('\nSalvando index.json...');
    const outputPath = path.resolve(__dirname, '../data/index.json');
    fs.writeFileSync(outputPath, JSON.stringify(index, null, 2));
    console.log(`Indexação completa em ${outputPath}`);
}

main();
