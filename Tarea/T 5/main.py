from libraries import *
from altman import Altman
from export_excel import export_excel_all
from financial_statements import Companies
from visualization import print_ratios, print_z_scores, z_score_plot



def main():

    print("Starting data processing...\n")

    companies = Companies(
        ["VZ", "MA", "BA", "V"],
        interval="1y"
    )

    # ---------- ALTAMN MODEL ----------
    
    altman = Altman(companies)

    # ---------- PRINTS ----------
    print_ratios(altman)
    print_z_scores(altman)

    # ---------- PLOT ----------
    z_df = altman.z_scores_df()
    z_score_plot(z_df, title="Altman Z-Scores Visualization")
    
    # ---------- Merton Model ----------
    

if __name__ == "__main__":
    main()