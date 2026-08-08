# Fase 1 - Infraestrutura, Docker e a Adoção do WSL 2

## Objetivo Arquitetural
Provisionar um ambiente de desenvolvimento e produção contêinerizado que suporte inferência de IA local sob restrições severas de hardware.

## A Adoção Estratégica do WSL 2
A formatação do sistema e a ausência temporária do Ubuntu Server nativo revelaram uma oportunidade para implementar o conceito de **Paridade entre Desenvolvimento e Produção**. O uso do Windows Subsystem for Linux (WSL 2) não é um mero *workaround*; é uma prática avançada de DevOps. 

O WSL 2 possui integração nativa com o CUDA. Isso significa que o ambiente de desenvolvimento no Windows consegue acessar a GPU com a mesma eficiência que o servidor Linux final terá. Quando o hardware for formatado para o Ubuntu Server definitivo, nenhuma linha de código ou configuração precisará ser alterada. O repositório funcionará como um pacote *plug-and-play*.

## Decisões Técnicas e Instruções

### `docker-compose.yml`
*   **Repasse de GPU:** A instrução `deploy.resources.reservations.devices` aciona o *NVIDIA Container Toolkit*. Ela garante o repasse direto (*passthrough*) da GPU para o contêiner do Ollama, vital para que os cálculos matriciais dos modelos quantizados (GGUF) ocorram na placa de vídeo e não no processador.
*   **Gestão de VRAM:** A instrução `OLLAMA_KEEP_ALIVE=5m` é crítica. A limitação física de 2GB de VRAM da GPU NVIDIA GeForce 940MX exige uma gestão agressiva de memória. Este comando força o motor a descarregar o modelo da VRAM após 5 minutos de inatividade, liberando espaço para o sistema operacional e outros fluxos do LangGraph.

### `Dockerfile` (API)
*   **Imagem Base:** `FROM python:3.11-slim` reduz drasticamente a superfície de ataque e o tamanho da imagem, economizando espaço em disco e RAM no host.
*   **Otimização de Cache:** `RUN pip install --no-cache-dir` impede que o Docker armazene arquivos temporários de instalação do Python, mantendo o contêiner leve.