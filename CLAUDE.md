# Contexto do repositório

Repositório exclusivo de **um cliente corretor de imóveis**. Guarda a identidade
visual, o histórico de criativos e o material de referência.

Leia `marca/MANUAL.md` antes de produzir qualquer peça.

## Regra inegociável

Todo anúncio de imóvel **deve exibir o número do CRECI** do corretor
(Lei 6.530/78 e Resolução COFECI 326/92). Peça sem CRECI não sai.

## Como a marca funciona aqui

Não existe design system fechado. Cada leva de criativos tem liberdade de
estilo, mood e cor dominante. O que é **fixo** está em `marca/MANUAL.md`:
logo, paleta base, tipografia e assinatura obrigatória.

Resumo: **marca travada, layout livre.**

## Estrutura

```
marca/
  MANUAL.md        regras fixas da identidade
  logos/           arquivos originais do logo
  referencias/     inspirações enviadas pelo cliente
criativos/
  AAAA-MM-slug/    uma pasta por leva
    brief.md       objetivo, formato, tom
    entregas/      arquivos finais
  _modelo/         template para copiar ao iniciar leva nova
```

## Fluxo de produção

1. Criar `criativos/AAAA-MM-slug/` copiando `_modelo/`
2. Preencher o `brief.md`
3. Gerar variações para aprovação (canvas `/design`, multi-prancheta)
4. Peça aprovada vira design no Canva, com brand kit aplicado, para o cliente editar
5. Salvar os finais em `entregas/` e commitar

## Ferramentas

- **Canva** (conectado): geração com brand kit, edição pelo cliente, export
- **`/design`**: canvas de aprovação com várias pranchetas lado a lado
- **`canvas-design`**: PNG/PDF estático
- **Gamma**: apresentações, book de imóvel, proposta para proprietário

## Importante

O container é temporário. Nada existe de verdade antes do `git push`.
Commitar sempre que a marca ou uma entrega mudar.
