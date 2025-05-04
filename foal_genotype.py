def generate_foal_genotype(mare_genotype, stallion_genotype):
    mare_genes = mare_genotype.split('/')
    stallion_genes = stallion_genotype.split('/')

# ========================
# Extentsion and Agouti
# ========================    

    # Randomly choose one allele from each parent for extension gene
    foal_extension_gene = random.choice([mare_genes[0][0], mare_genes[0][1]]) + random.choice([stallion_genes[0][0], stallion_genes[0][1]])
    
    # Randomly choose one allele from each parent for agouti gene
    foal_agouti_gene = random.choice([mare_genes[1][0], mare_genes[1][1]]) + random.choice([stallion_genes[1][0], stallion_genes[1][1]])


# ========================
# Positions of the genes
# ========================

zp_position_m = 2 if len(mare_genes) > 2 and 'Zp' in mare_genes[2] else None
zp_position_s = 2 if len(stallion_genes) > 2 and 'Zp' in stallion_genes[2] else None


zf_position_m = 3 if zp_position_m == 2 and len(mare_genes) > 3 and 'Zf' in mare_genes[3] else (
    2 if len(mare_genes) > 2 and 'Zf' in mare_genes[2] else None)
zf_position_s = 3 if zp_position_s == 2 and len(stallion_genes) > 3 and 'Zf' in stallion_genes[3] else (
    2 if len(stallion_genes) > 2 and 'Zf' in stallion_genes[2] else None)


zd_position_m = 4 if zp_position_m == 2 and zf_position_m == 3 and len(mare_genes) > 4 and 'Zd' in mare_genes[4] else (
    3 if len(mare_genes) > 3 and 'Zd' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'Zd' in mare_genes[2] else None)
zd_position_s = 4 if zp_position_s == 2 and zf_position_s == 3 and len(stallion_genes) > 4 and 'Zd' in stallion_genes[4] else (
    3 if len(stallion_genes) > 3 and 'Zd' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'Zd' in stallion_genes[2] else None)


cr_position_m = 5 if zp_position_m == 2 and zf_position_m == 3 and zd_position_m == 4 and p_position_m == 7 and len(mare_genes) > 5 and 'Cr' in mare_genes[5] else (
    4 if len(mare_genes) > 4 and 'Cr' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'Cr' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'Cr' in mare_genes[2] else None)
cr_position_s = 5 if zp_position_s == 2 and zf_position_s == 3 and zd_position_s == 4 and p_position_s == 7 and len(stallion_genes) > 5 and 'Cr' in stallion_genes[5] else (
    4 if len(stallion_genes) > 4 and 'Cr' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'Cr' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'Cr' in stallion_genes[2] else None)


ch_position_m = 6 if zp_position_m == 2 and zf_position_m == 3 and zd_position_m == 4 and p_position_m == 7 and cr_position_m == 5 and len(mare_genes) > 6 and 'Ch' in mare_genes[6] else (
    5 if len(mare_genes) > 5 and 'Ch' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'Ch' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'Ch' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'Ch' in mare_genes[2] else None)
ch_position_s = 6 if zp_position_s == 2 and zf_position_s == 3 and zd_position_s == 4 and p_position_s == 7 and cr_position_s == 5 and len(stallion_genes) > 6 and 'Ch' in stallion_genes[6] else (
    5 if len(stallion_genes) > 5 and 'Ch' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'Ch' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'Ch' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'Ch' in stallion_genes[2] else None)


p_position_m = 7 if zp_position_m == 2 and zf_position_m == 3 and zd_position_m == 4 and len(mare_genes) > 7 and 'P' in mare_genes[7] else (
    6 if len(mare_genes) > 6 and 'P' in mare_genes[6] else
    5 if len(mare_genes) > 5 and 'P' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'P' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'P' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'P' in mare_genes[2] else None)
p_position_s = 7 if zp_position_s == 2 and zf_position_s == 3 and zd_position_s == 4 and len(stallion_genes) > 7 and 'P' in stallion_genes[7] else (
    6 if len(stallion_genes) > 6 and 'P' in stallion_genes[6] else
    5 if len(stallion_genes) > 5 and 'P' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'P' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'P' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'P' in stallion_genes[2] else None)


sty_position_m = 8 if zp_position_m == 2 and zf_position_m == 3 and zd_position_m == 4 and cr_position_m == 5 and ch_position_m == 6 and p_position_m == 7 and len(mare_genes) > 8 and 'STY' in mare_genes[8] else (
    7 if len(mare_genes) > 7 and 'STY' in mare_genes[7] else
    6 if len(mare_genes) > 6 and 'STY' in mare_genes[6] else
    5 if len(mare_genes) > 5 and 'STY' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'STY' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'STY' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'STY' in mare_genes[2] else None)
sty_position_s = 8 if zp_position_s == 2 and zf_position_s == 3 and zd_position_s == 4 and cr_position_s == 5 and ch_position_s == 6 and p_position_s == 7 and len(stallion_genes) > 8 and 'STY' in stallion_genes[8] else (
    7 if len(stallion_genes) > 7 and 'STY' in stallion_genes[7] else
    6 if len(stallion_genes) > 6 and 'STY' in stallion_genes[6] else
    5 if len(stallion_genes) > 5 and 'STY' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'STY' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'STY' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'STY' in stallion_genes[2] else None)


rn_position_m = 9 if zp_position_m == 2 and zf_position_m == 3 and zd_position_m == 4 and cr_position_m == 5 and ch_position_m == 6 and p_position_m == 7 and sty_position_m == 8 and len(mare_genes) > 9 and 'RN' in mare_genes[9] else (
    8 if len(mare_genes) > 8 and 'RN' in mare_genes[8] else
    7 if len(mare_genes) > 7 and 'RN' in mare_genes[7] else
    6 if len(mare_genes) > 6 and 'RN' in mare_genes[6] else
    5 if len(mare_genes) > 5 and 'RN' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'RN' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'RN' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'RN' in mare_genes[2] else None)
rn_position_s = 9 if zp_position_s == 2 and zf_position_s == 3 and zd_position_s == 4 and cr_position_s == 5 and ch_position_s == 6 and p_position_s == 7 and sty_position_s == 8 and len(stallion_genes) > 9 and 'RN' in stallion_genes[9] else (
    8 if len(stallion_genes) > 8 and 'RN' in stallion_genes[8] else
    7 if len(stallion_genes) > 7 and 'RN' in stallion_genes[7] else
    6 if len(stallion_genes) > 6 and 'RN' in stallion_genes[6] else
    5 if len(stallion_genes) > 5 and 'RN' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'RN' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'RN' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'RN' in stallion_genes[2] else None)


g_position_m = 10 if zp_position_m == 2 and zf_position_m == 3 and zd_position_m == 4 and cr_position_m == 5 and ch_position_m == 6 and p_position_m == 7 and sty_position_m == 8 and rn_position_m == 9 and len(mare_genes) > 10 and 'G' in mare_genes[10] else (
    9 if len(mare_genes) > 9 and 'G' in mare_genes[9] else
    8 if len(mare_genes) > 8 and 'G' in mare_genes[8] else
    7 if len(mare_genes) > 7 and 'G' in mare_genes[7] else
    6 if len(mare_genes) > 6 and 'G' in mare_genes[6] else
    5 if len(mare_genes) > 5 and 'G' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'G' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'G' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'G' in mare_genes[2] else None)
g_position_s = 10 if zp_position_s == 2 and zf_position_s == 3 and zd_position_s == 4 and cr_position_s == 5 and ch_position_s == 6 and p_position_s == 7 and sty_position_s == 8 and rn_position_s == 9 and len(stallion_genes) > 10 and 'G' in stallion_genes[10] else (
    9 if len(stallion_genes) > 9 and 'G' in stallion_genes[9] else
    8 if len(stallion_genes) > 8 and 'G' in stallion_genes[8] else
    7 if len(stallion_genes) > 7 and 'G' in stallion_genes[7] else
    6 if len(stallion_genes) > 6 and 'G' in stallion_genes[6] else
    5 if len(stallion_genes) > 5 and 'G' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'G' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'G' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'G' in stallion_genes[2] else None)


z_position_m = 11 if zp_position_m == 2 and zf_position_m == 3 and zd_position_m == 4 and cr_position_m == 5 and ch_position_m == 6 and p_position_m == 7 and sty_position_m == 8 and rn_position_m == 9 and g_position_m == 10 and len(mare_genes) > 11 and 'Z' in mare_genes[11] else (
    10 if len(mare_genes) > 10 and 'Z' in mare_genes[10] else
    9 if len(mare_genes) > 9 and 'Z' in mare_genes[9] else
    8 if len(mare_genes) > 8 and 'Z' in mare_genes[8] else
    7 if len(mare_genes) > 7 and 'Z' in mare_genes[7] else
    6 if len(mare_genes) > 6 and 'Z' in mare_genes[6] else
    5 if len(mare_genes) > 5 and 'Z' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'Z' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'Z' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'Z' in mare_genes[2] else None)
z_position_s = 11 if zp_position_s == 2 and zf_position_s == 3 and zd_position_s == 4 and cr_position_s == 5 and ch_position_s == 6 and p_position_s == 7 and sty_position_s == 8 and rn_position_s == 9 and g_position_s == 10 and len(stallion_genes) > 11 and 'Z' in stallion_genes[11] else (
    10 if len(stallion_genes) > 10 and 'Z' in stallion_genes[10] else
    9 if len(stallion_genes) > 9 and 'Z' in stallion_genes[9] else
    8 if len(stallion_genes) > 8 and 'Z' in stallion_genes[8] else
    7 if len(stallion_genes) > 7 and 'Z' in stallion_genes[7] else
    6 if len(stallion_genes) > 6 and 'Z' in stallion_genes[6] else
    5 if len(stallion_genes) > 5 and 'Z' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'Z' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'Z' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'Z' in stallion_genes[2] else None)


lp_position_m = 12 if z_position_m == 11 and len(mare_genes) > 12 and 'Lp' in mare_genes[12] else (
    11 if len(mare_genes) > 11 and 'Lp' in mare_genes[11] else
    10 if len(mare_genes) > 10 and 'Lp' in mare_genes[10] else
    9 if len(mare_genes) > 9 and 'Lp' in mare_genes[9] else
    8 if len(mare_genes) > 8 and 'Lp' in mare_genes[8] else
    7 if len(mare_genes) > 7 and 'Lp' in mare_genes[7] else
    6 if len(mare_genes) > 6 and 'Lp' in mare_genes[6] else
    5 if len(mare_genes) > 5 and 'Lp' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'Lp' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'Lp' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'Lp' in mare_genes[2] else None)
lp_position_s = 12 if z_position_s == 11 and len(stallion_genes) > 12 and 'Lp' in stallion_genes[12] else (
    11 if len(stallion_genes) > 11 and 'Lp' in stallion_genes[11] else
    10 if len(stallion_genes) > 10 and 'Lp' in stallion_genes[10] else
    9 if len(stallion_genes) > 9 and 'Lp' in stallion_genes[9] else
    8 if len(stallion_genes) > 8 and 'Lp' in stallion_genes[8] else
    7 if len(stallion_genes) > 7 and 'Lp' in stallion_genes[7] else
    6 if len(stallion_genes) > 6 and 'Lp' in stallion_genes[6] else
    5 if len(stallion_genes) > 5 and 'Lp' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'Lp' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'Lp' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'Lp' in stallion_genes[2] else None)


to_position_m = 13 if lp_position_m == 12 and len(mare_genes) > 13 and 'To' in mare_genes[13] else (
    12 if len(mare_genes) > 12 and 'To' in mare_genes[12] else
    11 if len(mare_genes) > 11 and 'To' in mare_genes[11] else
    10 if len(mare_genes) > 10 and 'To' in mare_genes[10] else
    9 if len(mare_genes) > 9 and 'To' in mare_genes[9] else
    8 if len(mare_genes) > 8 and 'To' in mare_genes[8] else
    7 if len(mare_genes) > 7 and 'To' in mare_genes[7] else
    6 if len(mare_genes) > 6 and 'To' in mare_genes[6] else
    5 if len(mare_genes) > 5 and 'To' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'To' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'To' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'To' in mare_genes[2] else None)
to_position_s = 13 if lp_position_s == 12 and len(stallion_genes) > 13 and 'To' in stallion_genes[13] else (
    12 if len(stallion_genes) > 12 and 'To' in stallion_genes[12] else
    11 if len(stallion_genes) > 11 and 'To' in stallion_genes[11] else
    10 if len(stallion_genes) > 10 and 'To' in stallion_genes[10] else
    9 if len(stallion_genes) > 9 and 'To' in stallion_genes[9] else
    8 if len(stallion_genes) > 8 and 'To' in stallion_genes[8] else
    7 if len(stallion_genes) > 7 and 'To' in stallion_genes[7] else
    6 if len(stallion_genes) > 6 and 'To' in stallion_genes[6] else
    5 if len(stallion_genes) > 5 and 'To' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'To' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'To' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'To' in stallion_genes[2] else None)


sw_position_m = 14 if to_position_m == 13 and len(mare_genes) > 14 and 'Sw' in mare_genes[14] else (
    13 if len(mare_genes) > 13 and 'Sw' in mare_genes[13] else
    12 if len(mare_genes) > 12 and 'Sw' in mare_genes[12] else
    11 if len(mare_genes) > 11 and 'Sw' in mare_genes[11] else
    10 if len(mare_genes) > 10 and 'Sw' in mare_genes[10] else
    9 if len(mare_genes) > 9 and 'Sw' in mare_genes[9] else
    8 if len(mare_genes) > 8 and 'Sw' in mare_genes[8] else
    7 if len(mare_genes) > 7 and 'Sw' in mare_genes[7] else
    6 if len(mare_genes) > 6 and 'Sw' in mare_genes[6] else
    5 if len(mare_genes) > 5 and 'Sw' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'Sw' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'Sw' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'Sw' in mare_genes[2] else None)
sw_position_s = 14 if to_position_s == 13 and len(stallion_genes) > 14 and 'Sw' in stallion_genes[14] else (
    13 if len(stallion_genes) > 13 and 'Sw' in stallion_genes[13] else
    12 if len(stallion_genes) > 12 and 'Sw' in stallion_genes[12] else
    11 if len(stallion_genes) > 11 and 'Sw' in stallion_genes[11] else
    10 if len(stallion_genes) > 10 and 'Sw' in stallion_genes[10] else
    9 if len(stallion_genes) > 9 and 'Sw' in stallion_genes[9] else
    8 if len(stallion_genes) > 8 and 'Sw' in stallion_genes[8] else
    7 if len(stallion_genes) > 7 and 'Sw' in stallion_genes[7] else
    6 if len(stallion_genes) > 6 and 'Sw' in stallion_genes[6] else
    5 if len(stallion_genes) > 5 and 'Sw' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'Sw' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'Sw' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'Sw' in stallion_genes[2] else None)


sb_position_m = 15 if sw_position_m == 14 and len(mare_genes) > 15 and 'Sb' in mare_genes[15] else (
    14 if len(mare_genes) > 14 and 'Sb' in mare_genes[14] else
    13 if len(mare_genes) > 13 and 'Sb' in mare_genes[13] else
    12 if len(mare_genes) > 12 and 'Sb' in mare_genes[12] else
    11 if len(mare_genes) > 11 and 'Sb' in mare_genes[11] else
    10 if len(mare_genes) > 10 and 'Sb' in mare_genes[10] else
    9 if len(mare_genes) > 9 and 'Sb' in mare_genes[9] else
    8 if len(mare_genes) > 8 and 'Sb' in mare_genes[8] else
    7 if len(mare_genes) > 7 and 'Sb' in mare_genes[7] else
    6 if len(mare_genes) > 6 and 'Sb' in mare_genes[6] else
    5 if len(mare_genes) > 5 and 'Sb' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'Sb' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'Sb' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'Sb' in mare_genes[2] else None)
sb_position_s = 15 if sw_position_s == 14 and len(stallion_genes) > 15 and 'Sb' in stallion_genes[15] else (
    14 if len(stallion_genes) > 14 and 'Sb' in stallion_genes[14] else
    13 if len(stallion_genes) > 13 and 'Sb' in stallion_genes[13] else
    12 if len(stallion_genes) > 12 and 'Sb' in stallion_genes[12] else
    11 if len(stallion_genes) > 11 and 'Sb' in stallion_genes[11] else
    10 if len(stallion_genes) > 10 and 'Sb' in stallion_genes[10] else
    9 if len(stallion_genes) > 9 and 'Sb' in stallion_genes[9] else
    8 if len(stallion_genes) > 8 and 'Sb' in stallion_genes[8] else
    7 if len(stallion_genes) > 7 and 'Sb' in stallion_genes[7] else
    6 if len(stallion_genes) > 6 and 'Sb' in stallion_genes[6] else
    5 if len(stallion_genes) > 5 and 'Sb' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'Sb' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'Sb' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'Sb' in stallion_genes[2] else None)


o_position_m = 16 if sb_position_m == 15 and len(mare_genes) > 16 and 'O' in mare_genes[16] else (
    15 if len(mare_genes) > 15 and 'O' in mare_genes[15] else
    14 if len(mare_genes) > 14 and 'O' in mare_genes[14] else
    13 if len(mare_genes) > 13 and 'O' in mare_genes[13] else
    12 if len(mare_genes) > 12 and 'O' in mare_genes[12] else
    11 if len(mare_genes) > 11 and 'O' in mare_genes[11] else
    10 if len(mare_genes) > 10 and 'O' in mare_genes[10] else
    9 if len(mare_genes) > 9 and 'O' in mare_genes[9] else
    8 if len(mare_genes) > 8 and 'O' in mare_genes[8] else
    7 if len(mare_genes) > 7 and 'O' in mare_genes[7] else
    6 if len(mare_genes) > 6 and 'O' in mare_genes[6] else
    5 if len(mare_genes) > 5 and 'O' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'O' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'O' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'O' in mare_genes[2] else None)
o_position_s = 16 if sb_position_s == 15 and len(stallion_genes) > 16 and 'O' in stallion_genes[16] else (
    15 if len(stallion_genes) > 15 and 'O' in stallion_genes[15] else
    14 if len(stallion_genes) > 14 and 'O' in stallion_genes[14] else
    13 if len(stallion_genes) > 13 and 'O' in stallion_genes[13] else
    12 if len(stallion_genes) > 12 and 'O' in stallion_genes[12] else
    11 if len(stallion_genes) > 11 and 'O' in stallion_genes[11] else
    10 if len(stallion_genes) > 10 and 'O' in stallion_genes[10] else
    9 if len(stallion_genes) > 9 and 'O' in stallion_genes[9] else
    8 if len(stallion_genes) > 8 and 'O' in stallion_genes[8] else
    7 if len(stallion_genes) > 7 and 'O' in stallion_genes[7] else
    6 if len(stallion_genes) > 6 and 'O' in stallion_genes[6] else
    5 if len(stallion_genes) > 5 and 'O' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'O' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'O' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'O' in stallion_genes[2] else None)


rb_position_m = 17 if o_position_m == 16 and len(mare_genes) > 17 and 'Rb' in mare_genes[17] else (
    16 if len(mare_genes) > 16 and 'Rb' in mare_genes[16] else
    15 if len(mare_genes) > 15 and 'Rb' in mare_genes[15] else
    14 if len(mare_genes) > 14 and 'Rb' in mare_genes[14] else
    13 if len(mare_genes) > 13 and 'Rb' in mare_genes[13] else
    12 if len(mare_genes) > 12 and 'Rb' in mare_genes[12] else
    11 if len(mare_genes) > 11 and 'Rb' in mare_genes[11] else
    10 if len(mare_genes) > 10 and 'Rb' in mare_genes[10] else
    9 if len(mare_genes) > 9 and 'Rb' in mare_genes[9] else
    8 if len(mare_genes) > 8 and 'Rb' in mare_genes[8] else
    7 if len(mare_genes) > 7 and 'Rb' in mare_genes[7] else
    6 if len(mare_genes) > 6 and 'Rb' in mare_genes[6] else
    5 if len(mare_genes) > 5 and 'Rb' in mare_genes[5] else
    4 if len(mare_genes) > 4 and 'Rb' in mare_genes[4] else
    3 if len(mare_genes) > 3 and 'Rb' in mare_genes[3] else
    2 if len(mare_genes) > 2 and 'Rb' in mare_genes[2] else None)
rb_position_s = 17 if o_position_s == 16 and len(stallion_genes) > 17 and 'Rb' in stallion_genes[17] else (
    16 if len(stallion_genes) > 16 and 'Rb' in stallion_genes[16] else
    15 if len(stallion_genes) > 15 and 'Rb' in stallion_genes[15] else
    14 if len(stallion_genes) > 14 and 'Rb' in stallion_genes[14] else
    13 if len(stallion_genes) > 13 and 'Rb' in stallion_genes[13] else
    12 if len(stallion_genes) > 12 and 'Rb' in stallion_genes[12] else
    11 if len(stallion_genes) > 11 and 'Rb' in stallion_genes[11] else
    10 if len(stallion_genes) > 10 and 'Rb' in stallion_genes[10] else
    9 if len(stallion_genes) > 9 and 'Rb' in stallion_genes[9] else
    8 if len(stallion_genes) > 8 and 'Rb' in stallion_genes[8] else
    7 if len(stallion_genes) > 7 and 'Rb' in stallion_genes[7] else
    6 if len(stallion_genes) > 6 and 'Rb' in stallion_genes[6] else
    5 if len(stallion_genes) > 5 and 'Rb' in stallion_genes[5] else
    4 if len(stallion_genes) > 4 and 'Rb' in stallion_genes[4] else
    3 if len(stallion_genes) > 3 and 'Rb' in stallion_genes[3] else
    2 if len(stallion_genes) > 2 and 'Rb' in stallion_genes[2] else None)



# ========================
# Patterning (Zp)
# ========================

if zp_position_m is not None and len(mare_genes) > zp_position_m:
    mare_zp_allele = random.choice([mare_genes[zp_position_m][0:2], mare_genes[zp_position_m][2:]])
else:
    mare_zp_allele = ""

if zp_position_s is not None and len(stallion_genes) > zp_position_s:
    stallion_zp_allele = random.choice([stallion_genes[zp_position_s][0:2], stallion_genes[zp_position_s][2:]])
else:
    stallion_zp_allele = ""

foal_zp_gene = mare_zp_allele + stallion_zp_allele

if foal_zp_gene == 'zpzp' or foal_zp_gene == 'zp':
    foal_zp_gene = ""
elif foal_zp_gene == 'Zpzp' or foal_zp_gene == 'zpZp' or foal_zp_gene == 'Zp':
    foal_zp_gene = "Zpzp"
elif foal_zp_gene == 'ZpZp':
    foal_zp_gene = "ZpZp"


# ========================
# Zebra Fusion (Zf)
# ========================

if zf_position_m is not None and len(mare_genes) > zf_position_m:
    mare_zf_allele = random.choice([mare_genes[zf_position_m][0:2], mare_genes[zf_position_m][2:]])
else:
    mare_zf_allele = ""

if zf_position_s is not None and len(stallion_genes) > zf_position_s:
    stallion_zf_allele = random.choice([stallion_genes[zf_position_s][0:2], stallion_genes[zf_position_s][2:]])
else:
    stallion_zf_allele = ""

foal_zf_gene = mare_zf_allele + stallion_zf_allele

if foal_zf_gene == 'zfzf' or foal_zf_gene == 'zf':
    foal_zf_gene = ""
elif foal_zf_gene == 'Zfzf' or foal_zf_gene == 'zfZf' or foal_zf_gene == 'Zf':
    foal_zf_gene = "Zfzf"
elif foal_zf_gene == 'ZfZf':
    foal_zf_gene = "ZfZf"


# ========================
# Zebra Dilution (Zd)
# ========================

if zd_position_m is not None and len(mare_genes) > zd_position_m:
    mare_zd_allele = random.choice([mare_genes[zd_position_m][0:2], mare_genes[zd_position_m][2:]])
else:
    mare_zd_allele = ""

if zd_position_s is not None and len(stallion_genes) > zd_position_s:
    stallion_zd_allele = random.choice([stallion_genes[zd_position_s][0:2], stallion_genes[zd_position_s][2:]])
else:
    stallion_zd_allele = ""

foal_zd_gene = mare_zd_allele + stallion_zd_allele

if foal_zd_gene == 'zdzd' or foal_zd_gene == 'zd':
    foal_zd_gene = ""
elif foal_zd_gene == 'Zdzd' or foal_zd_gene == 'zdZd' or foal_zd_gene == 'Zd':
    foal_zd_gene = "Zdzd"
elif foal_zd_gene == 'ZdZd':
    foal_zd_gene = "ZdZd"


# ========================
# Cream (CR)
# ========================
        
if cr_position_m is not None and len(mare_genes) > cr_position_m:
    mare_cream_allele = random.choice([mare_genes[cr_position_m][0:2], mare_genes[cr_position_m][2:]])
else:
    mare_cream_allele = ""

if cr_position_s is not None and len(stallion_genes) > cr_position_s:
    stallion_cream_allele = random.choice([stallion_genes[cr_position_s][0:2], stallion_genes[cr_position_s][2:]])
else:
    stallion_cream_allele = ""

foal_cream_gene = mare_cream_allele + stallion_cream_allele

if foal_cream_gene in ['crcr', 'cr']:
    foal_cream_gene = ""
elif foal_cream_gene in ['Crcr', 'crCr', 'Cr']:
    foal_cream_gene = "Crcr"
elif foal_cream_gene == 'CrCr':
    foal_cream_gene = "CrCr"


# ========================
# Champagne
# ========================

if ch_position_m is not None and len(mare_genes) > ch_position_m:
    mare_champ_allele = random.choice([mare_genes[ch_position_m][0:2], mare_genes[ch_position_m][2:]])
else:
    mare_champ_allele = ""

if ch_position_s is not None and len(stallion_genes) > ch_position_s:
    stallion_champ_allele = random.choice([stallion_genes[ch_position_s][0:2], stallion_genes[ch_position_s][2:]])
else:
    stallion_champ_allele = ""

foal_champ_gene = mare_champ_allele + stallion_champ_allele

if foal_champ_gene == 'chch' or foal_champ_gene == 'ch':
    foal_champ_gene = ""
elif foal_champ_gene == 'Chch' or foal_champ_gene == 'chCh' or foal_champ_gene == 'Ch':
    foal_champ_gene = "Chch"
elif foal_champ_gene == 'ChCh':
    foal_champ_gene = "ChCh"


# ========================
# Pangare
# ========================
    
    if p_position_m is not None and len(mare_genes) > p_position_m:
        mare_pangare_allele = random.choice([mare_genes[p_position_m][0], mare_genes[p_position_m][1]])      
    else:
        mare_pangare_allele = ""

    if p_position_s is not None and len(stallion_genes) > p_position_s:
        stallion_pangare_allele = random.choice([stallion_genes[p_position_s][0], stallion_genes[p_position_s][1]])  
    else:
        stallion_pangare_allele = ""

    foal_pangare_gene = mare_pangare_allele + stallion_pangare_allele

    if foal_pangare_gene == 'pp' or foal_pangare_gene == 'p':
        foal_pangare_gene = ""
    elif foal_pangare_gene == 'Pp' or foal_pangare_gene == 'pP' or foal_pangare_gene == 'P':
        foal_pangare_gene = "Pp"
    elif foal_pangare_gene == 'PP':
        foal_pangare_gene = "PP"


# ========================
# Sooty (Sty)
# ======================== 

if sty_position_m is not None and len(mare_genes) > sty_position_m:
    mare_sooty_allele = random.choice([mare_genes[sty_position_m][0:3], mare_genes[sty_position_m][3:]])
else:
    mare_sooty_allele = ""

if sty_position_s is not None and len(stallion_genes) > sty_position_s:
    stallion_sooty_allele = random.choice([stallion_genes[sty_position_s][0:3], stallion_genes[sty_position_s][3:]])
else:
    stallion_sooty_allele = ""

foal_sooty_gene = mare_sooty_allele + stallion_sooty_allele

if foal_sooty_gene == 'stysty' or foal_sooty_gene == 'sty':
    foal_sooty_gene = ""
elif foal_sooty_gene == 'Stysty' or foal_sooty_gene == 'stySty' or foal_sooty_gene == 'Sty':
    foal_sooty_gene = "Stysty"
elif foal_sooty_gene == 'StySty':
    foal_sooty_gene = "StySty"
        

# ========================
# Roan (Rn)
# ========================

if rn_position_m is not None and len(mare_genes) > rn_position_m:
    mare_roan_allele = random.choice([mare_genes[rn_position_m][0:2], mare_genes[rn_position_m][2:]])
else:
    mare_roan_allele = ""

if rn_position_s is not None and len(stallion_genes) > rn_position_s:
    stallion_roan_allele = random.choice([stallion_genes[rn_position_s][0:2], stallion_genes[rn_position_s][2:]])
else:
    stallion_roan_allele = ""

foal_roan_gene = mare_roan_allele + stallion_roan_allele

if foal_roan_gene == 'rnrn' or foal_roan_gene == 'rn':
    foal_roan_gene = ""
elif foal_roan_gene == 'Rnrn' or foal_roan_gene == 'rnRn' or foal_roan_gene == 'Rn':
    foal_roan_gene = "Rnrn"
elif foal_roan_gene == 'RnRn':
    foal_roan_gene = "RnRn"


# ========================
# Grey
# ========================
        
    if g_position_m is not None and len(mare_genes) > g_position_m:
        mare_grey_allele = random.choice([mare_genes[g_position_m][0], mare_genes[g_position_m][1]])
    else:
        mare_grey_allele = ""

    if g_position_s is not None and len(stallion_genes) > g_position_s:
        stallion_grey_allele = random.choice([stallion_genes[g_position_s][0], stallion_genes[g_position_s][1]])
    else:
        stallion_grey_allele = ""

    foal_grey_gene = mare_grey_allele + stallion_grey_allele

    if foal_grey_gene == 'gg' or foal_grey_gene == 'g':
        foal_grey_gene = ""
    elif foal_grey_gene == 'Gg' or foal_grey_gene == 'gG' or foal_grey_gene == 'G':
        foal_grey_gene = "Gg"
    elif foal_grey_gene == 'GG':
        foal_grey_gene = "GG"


# ========================
# Silver (Z)
# ========================

if z_position_m is not None and len(mare_genes) > z_position_m:
    mare_silver_allele = random.choice([mare_genes[z_position_m][0], mare_genes[z_position_m][1]])      
else:
    mare_silver_allele = ""

if z_position_s is not None and len(stallion_genes) > z_position_s:
    stallion_silver_allele = random.choice([stallion_genes[z_position_s][0], stallion_genes[z_position_s][1]])  
else:
    stallion_silver_allele = ""

foal_silver_gene = mare_silver_allele + stallion_silver_allele

if foal_silver_gene == 'zz' or foal_silver_gene == 'z':
    foal_silver_gene = ""
elif foal_silver_gene in ['Zz', 'zZ', 'Z']:
    foal_silver_gene = "Zz"
elif foal_silver_gene == 'ZZ':
    foal_silver_gene = "ZZ"


# ========================
# Appaloosa (Lp)
# ========================

if lp_position_m is not None and len(mare_genes) > lp_position_m:
    mare_appy_allele = random.choice([mare_genes[lp_position_m][0:2], mare_genes[lp_position_m][2:]])
else:
    mare_appy_allele = ""

if lp_position_s is not None and len(stallion_genes) > lp_position_s:
    stallion_appy_allele = random.choice([stallion_genes[lp_position_s][0:2], stallion_genes[lp_position_s][2:]])
else:
    stallion_appy_allele = ""

foal_appy_gene = mare_appy_allele + stallion_appy_allele

if foal_appy_gene == 'lplp' or foal_appy_gene == 'lp':
    foal_appy_gene = ""
elif foal_appy_gene in ['Lplp', 'lpLp', 'Lp']:
    foal_appy_gene = "Lplp"
elif foal_appy_gene == 'LpLp':
    foal_appy_gene = "LpLp"


# ========================
# Tobiano
# ========================

    if to_position_m is not None and len(mare_genes) > to_position_m:
        mare_tobi_allele = random.choice([mare_genes[to_position_m][0:2], mare_genes[to_position_m][2:]])
    else:
        mare_tobi_allele = ""

    if to_position_s is not None and len(stallion_genes) > to_position_s:
        stallion_tobi_allele = random.choice([stallion_genes[to_position_s][0:2], stallion_genes[to_position_s][2:]])
    else:
        stallion_tobi_allele = ""

    foal_tobi_gene = mare_tobi_allele + stallion_tobi_allele

    if foal_tobi_gene == 'toto' or foal_tobi_gene == 'to':
        foal_tobi_gene = ""
    elif foal_tobi_gene == 'Toto' or foal_tobi_gene == 'toTo' or foal_tobi_gene == 'To':
        foal_tobi_gene = "Toto"
    elif foal_tobi_gene == 'ToTo':
        foal_tobi_gene = "ToTo"
    


# ========================
# Sabino
# ========================

    if sb_position_m is not None and len(mare_genes) > sb_position_m:
        mare_sab_allele = random.choice([mare_genes[sb_position_m][0:2], mare_genes[sb_position_m][2:]])
    else:
        mare_sab_allele = ""

    if sb_position_s is not None and len(stallion_genes) > sb_position_s:
        stallion_sab_allele = random.choice([stallion_genes[sb_position_s][0:2], stallion_genes[sb_position_s][2:]])
    else:
        stallion_sab_allele = ""

    foal_sab_gene = mare_sab_allele + stallion_sab_allele

    if foal_sab_gene == 'sbsb' or foal_sab_gene == 'sb':
        foal_sab_gene = ""
    elif foal_sab_gene == 'Sbsb' or foal_sab_gene == 'sbSb' or foal_sab_gene == 'Sb':
        foal_sab_gene = "Sbsb"
    elif foal_sab_gene == 'SbSb':
        foal_sab_gene = "SbSb"


# ========================
# Overo (O)
# ========================

if o_position_m is not None and len(mare_genes) > o_position_m:
    mare_overo_allele = random.choice([mare_genes[o_position_m][0:1], mare_genes[o_position_m][1:]])
else:
    mare_overo_allele = ""

if o_position_s is not None and len(stallion_genes) > o_position_s:
    stallion_overo_allele = random.choice([stallion_genes[o_position_s][0:1], stallion_genes[o_position_s][1:]])
else:
    stallion_overo_allele = ""

foal_overo_gene = mare_overo_allele + stallion_overo_allele

if foal_overo_gene in ['oo', 'o']:
    foal_overo_gene = ""
elif foal_overo_gene in ['Oo', 'oO', 'O']:
    foal_overo_gene = "Oo"
elif foal_overo_gene == 'OO':
    foal_overo_gene = "OO"

    
# ========================
# Splash White (SW)
# ========================

if sw_position_m is not None and len(mare_genes) > sw_position_m:
    mare_sw_allele = random.choice([mare_genes[sw_position_m][0:2], mare_genes[sw_position_m][2:]])
else:
    mare_sw_allele = ""

if sw_position_s is not None and len(stallion_genes) > sw_position_s:
    stallion_sw_allele = random.choice([stallion_genes[sw_position_s][0:2], stallion_genes[sw_position_s][2:]])
else:
    stallion_sw_allele = ""

foal_sw_gene = mare_sw_allele + stallion_sw_allele

if foal_sw_gene in ['swsw', 'sw']:
    foal_sw_gene = ""
elif foal_sw_gene in ['Swsw', 'swSw', 'Sw']:
    foal_sw_gene = "Swsw"
elif foal_sw_gene == 'SwSw':
    foal_sw_gene = "SwSw"


# ========================
# Rabicano (RB)
# ========================

if rb_position_m is not None and len(mare_genes) > rb_position_m:
    mare_rb_allele = random.choice([mare_genes[rb_position_m][0:2], mare_genes[rb_position_m][2:]])
else:
    mare_rb_allele = ""

if rb_position_s is not None and len(stallion_genes) > rb_position_s:
    stallion_rb_allele = random.choice([stallion_genes[rb_position_s][0:2], stallion_genes[rb_position_s][2:]])
else:
    stallion_rb_allele = ""

foal_rb_gene = mare_rb_allele + stallion_rb_allele

if foal_rb_gene in ['rbrb', 'rb']:
    foal_rb_gene = ""
elif foal_rb_gene in ['Rbrb', 'rbRb', 'Rb']:
    foal_rb_gene = "Rbrb"
elif foal_rb_gene == 'RbRb':
    foal_rb_gene = "RbRb"




# ========================
# Geno generation
# ========================
    # Combine the selected genes to create the foal's genotype
    foal_genotype = f"{foal_extension_gene}/{foal_agouti_gene}"
if foal_zp_gene:
    foal_genotype += f"/{foal_zp_gene}"
if foal_zf_gene:
    foal_genotype += f"/{foal_zf_gene}"
if foal_zd_gene:
    foal_genotype += f"/{foal_zd_gene}"
if foal_cream_gene:
    foal_genotype += f"/{foal_cream_gene}"
if foal_champ_gene:
    foal_genotype += f"/{foal_champ_gene}"
if foal_pangare_gene:
    foal_genotype += f"/{foal_pangare_gene}"
if foal_sooty_gene:
    foal_genotype += f"/{foal_sooty_gene}"
if foal_roan_gene:
    foal_genotype += f"/{foal_roan_gene}"
if foal_grey_gene:
    foal_genotype += f"/{foal_grey_gene}"
if foal_silver_gene:
    foal_genotype += f"/{foal_silver_gene}"
if foal_appy_gene:
    foal_genotype += f"/{foal_appy_gene}"
if foal_tobi_gene:
    foal_genotype += f"/{foal_tobi_gene}"
if foal_sab_gene:
    foal_genotype += f"/{foal_sab_gene}"
if foal_overo_gene:
    foal_genotype += f"/{foal_overo_gene}"
if foal_sw_gene:
    foal_genotype += f"/{foal_sw_gene}"
if foal_rb_gene:
    foal_genotype += f"/{foal_rb_gene}"

    return foal_genotype
